"""Copyright Alpine Intuition Sàrl team.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from functools import wraps
from typing import Dict, List, Union

import psutil
from py3nvml import py3nvml

try:
    py3nvml.nvmlInit()
    GPUS_AVAILABLE = True
    NUM_GPUS = py3nvml.nvmlDeviceGetCount()
except (py3nvml.NVMLError_DriverNotLoaded, py3nvml.NVMLError_LibraryNotFound):
    GPUS_AVAILABLE = False
    NUM_GPUS = 0


def are_gpus_available(func):
    """Decorator to check if gpus are are_gpus_available."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not GPUS_AVAILABLE:
            raise RuntimeError("Cannot use GPU utilities")
        return func(*args, **kwargs)

    return wrapper


def get_num_gpus() -> int:
    """Get the number of available gpus.

    Args:
        None

    Returns:
        number of gpus

    Raises:
        None
    """
    return NUM_GPUS


@are_gpus_available
def get_device_vram_usage(device_id: int, free: bool = False) -> int:
    """Get GPU VRAM usage (in MB) for one specific device.

    Args:
        device_id: id of the needed asked
        free: if false, return used memory, if true return free available memory

    Returns:
        VRAM usage (free or used) in MiB

    Raises:
        ValueError: invalid device id
    """

    if NUM_GPUS == 0:
        return 0

    if device_id > NUM_GPUS - 1 or device_id < 0:
        raise ValueError(f"Invalid device id: {device_id}")

    handle = py3nvml.nvmlDeviceGetHandleByIndex(device_id)
    info = py3nvml.nvmlDeviceGetMemoryInfo(handle)

    return info.free >> 20 if free else info.used >> 20


@are_gpus_available
def get_devices_vram_usage(free: bool = False) -> List[int]:
    """Get GPU VRAM usage (in MB) for all specific devices.

    Args:
        free: if false, return used memory, if true return free available memory

    Returns:
        list of VRAM usage

    Raises:
        None.

    """
    return [get_device_vram_usage(i, free) for i in range(NUM_GPUS)]


@are_gpus_available
def get_vram_usages(pids: Union[int, List[int]]) -> Dict[int, int]:
    """Get GPU VRAM usage (in MB) for one or more pids.

    Args:
        pids: a pid or a list of pids.

    Returns:
        usages: a dictionnary of VRAM usage for the each given pids.

    Raises:
        None.
    """

    if isinstance(pids, int):
        pids = [pids]

    usages = {}
    for i in range(NUM_GPUS):
        handle = py3nvml.nvmlDeviceGetHandleByIndex(i)
        for proc in py3nvml.nvmlDeviceGetComputeRunningProcesses(handle):
            if proc.pid not in pids:
                continue
            usages[proc.pid] = proc.usedGpuMemory

    for pid in pids:
        if pid not in usages:
            usages[pid] = 0

    return usages


def get_ram_usages(pids: Union[int, List[int]]) -> Dict[int, Dict[str, int]]:
    """Get RAM memory usage (in MB) for one or more pids.

    Args:
        pids: a pid or a list of pids.

    Returns:
        usage: A list of RAM usage for the input PID list.

    Raises:
        None.
    """

    if isinstance(pids, int):
        pids = [pids]

    usages = {}
    for pid in pids:
        try:
            memory = psutil.Process(pid).memory_info()
            virt_ram, used_ram = memory.vms >> 20, memory.rss >> 20
        except psutil.NoSuchProcess:
            virt_ram, used_ram = 0, 0
        usages[pid] = {"virt": virt_ram, "used": used_ram}

    return usages
