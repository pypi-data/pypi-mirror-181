import copy
import dataclasses
import logging
import statistics
import time
import typing
import torch
import irisml.core
from irisml.tasks.train.build_dataloader import build_dataloader
from irisml.tasks.train.plugin_list import PluginList
from irisml.tasks.train.plugin_loader import load_plugin

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Benchmark a given model using a given dataset.

    Config:
        batch_size (int)
        device (Optional['cpu' or 'cuda']): If not provided, cuda is selected when CUDA is available.
        num_iterations (int): The number of iterations to run.
        skip_prediction (bool): If true, prediction steps are skipped and prediction_time_per_iteration will be zero.
    """
    VERSION = '0.1.3'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Inputs:
        model: torch.nn.Module
        dataset: torch.utils.data.Dataset
        transform: typing.Callable

    @dataclasses.dataclass
    class Config:
        batch_size: int
        device: typing.Optional[typing.Literal['cpu', 'cuda']] = None
        num_iterations: int = 10
        skip_prediction: bool = False
        plugins: typing.List[str] = dataclasses.field(default_factory=list)

    @dataclasses.dataclass
    class Outputs:
        forward_backward_time_per_iteration: float = 0.0
        forward_time_per_iteration: float = 0.0
        backward_time_per_iteration: float = 0.0
        prediction_time_per_iteration: float = 0.0
        max_cuda_memory_in_mb: float = 0.0

    def execute(self, inputs):
        plugins = PluginList([load_plugin(p, self.context) for p in self.config.plugins])
        device = self._get_device()
        self.device = device  # TODO: Better to make a trainer object.
        dataloader = build_dataloader(inputs.dataset, inputs.transform, batch_size=self.config.batch_size, shuffle=False, drop_last=False)
        forward_time_all = []
        backward_time_all = []
        prediction_time_all = []

        model = copy.deepcopy(inputs.model)
        if device.type == 'cuda':
            torch.cuda.reset_peak_memory_stats(device)
            cuda_memory_at_start = torch.cuda.memory_allocated(device)

        model.to(device)
        model.train()

        plugins.on_train_start(self, model)
        plugins.on_train_epoch_start(self, model, epoch_index=0)

        # Measure training forward and backward pass
        for i, batch in enumerate(dataloader):
            batch = plugins.on_train_batch_start(self, model, batch, i)

            inputs, targets = batch
            inputs = self._to_device(inputs, device)
            targets = self._to_device(targets, device)

            loss, forward_time, backward_time = self._training_step(model, inputs, targets, device, plugins)
            plugins.on_train_batch_end(self, model, loss, batch, i)
            forward_time_all.append(forward_time)
            backward_time_all.append(backward_time)
            if i >= self.config.num_iterations:
                break

        plugins.on_train_epoch_end(self, model, epoch_index=0)
        plugins.on_train_end(self, model)

        if not self.config.skip_prediction:
            model.eval()
            # Measure prediction time.
            for i, batch in enumerate(dataloader):
                inputs, targets = batch
                inputs = self._to_device(inputs, device)
                prediction_time_all.append(self._prediction_step(model, inputs, device))
                if i >= self.config.num_iterations:
                    break

        if len(forward_time_all) < self.config.num_iterations:
            logger.info(f"The dataset is smaller than expected. The actual number of iteration is {len(forward_time_all)}")

        forward_time_per_iteration = statistics.fmean(forward_time_all)
        backward_time_per_iteration = statistics.fmean(backward_time_all)
        forward_backward_time_per_iteration = forward_time_per_iteration + backward_time_per_iteration
        prediction_time_per_iteration = statistics.fmean(prediction_time_all) if prediction_time_all else 0
        max_cuda_memory_in_mb = ((torch.cuda.max_memory_allocated(device) - cuda_memory_at_start) / 2 ** 20) if device.type == 'cuda' else 0

        logger.info(f"{forward_time_per_iteration=}, {backward_time_per_iteration=}, {forward_backward_time_per_iteration=}, {prediction_time_per_iteration=}")
        if max_cuda_memory_in_mb > 0:
            logger.info(f"{max_cuda_memory_in_mb=}")

        return self.Outputs(forward_backward_time_per_iteration, forward_time_per_iteration, backward_time_per_iteration, prediction_time_per_iteration, max_cuda_memory_in_mb)

    def _get_device(self) -> torch.device:
        """Get a torch device based on the configuration. If not specified explicitly, it uses cuda if available."""
        if self.config.device:
            device_name = self.config.device
        else:
            device_name = 'cuda' if torch.cuda.is_available() else 'cpu'
            logger.info(f"Training device is selected automatically: {device_name}. To specify the device manually, please set Config.device.")

        return torch.device(device_name)

    def _to_device(self, data, device):
        if isinstance(data, list):
            return [self._to_device(d, device) for d in data]
        elif isinstance(data, tuple):
            return tuple(self._to_device(d, device) for d in data)
        elif hasattr(data, 'to'):
            return data.to(device, non_blocking=True)
        return data

    @staticmethod
    def _synchronize(device):
        if device.type == 'cuda':
            torch.cuda.synchronize()

    def _training_step(self, model, inputs, targets, device, plugins):
        self._synchronize(device)

        start = time.time()
        with plugins.forward_context():
            if hasattr(model, 'training_step'):
                loss = model.training_step(inputs, targets)['loss']
            else:
                loss = model.criterion(model(inputs), targets)

        self._synchronize(device)
        forward_time = time.time() - start
        loss = plugins.on_train_backward_start(self, model, loss)

        start = time.time()
        loss.backward()
        self._synchronize(device)
        backward_time = time.time() - start

        return loss, forward_time, backward_time

    def _prediction_step(self, model, inputs, device):
        self._synchronize(device)
        start = time.time()
        if hasattr(model, 'prediction_step'):
            model.prediction_step(inputs)
        elif hasattr(model, 'predictor'):
            model.predictor(model(inputs))
        else:
            model(inputs)
        self._synchronize(device)
        return time.time() - start
