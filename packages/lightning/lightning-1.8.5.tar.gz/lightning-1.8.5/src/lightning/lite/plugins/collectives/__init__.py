from lightning.lite.plugins.collectives.collective import Collective
from lightning.lite.plugins.collectives.single_device import SingleDeviceCollective
from lightning.lite.plugins.collectives.torch_collective import TorchCollective

__all__ = [
    "Collective",
    "TorchCollective",
    "SingleDeviceCollective",
]
