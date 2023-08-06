import math
import GPUtil
import psutil
import time

from threading import Thread
from typeguard import typechecked
from typing import List, Optional, Tuple

from .log import EventLogger


KEY_PREFIX = 'pyraisys_'


class SystemMetricsReporter:

    @typechecked
    def __init__(self, logger: EventLogger, interval: float, initial_wait: float = 3):
        assert interval >= 1
        assert initial_wait >= 0

        self.logger = logger
        self.interval = interval
        self.initial_wait = initial_wait
        self.gputil_success = True

        self.alive = True
        self.worker = Thread(target=self._worker_run, daemon=True)
        self.worker.start()


    def close(self):
        self.alive = False


    def __del__(self):
        self.close()


    def _worker_run(self):
        # wait a number of seconds before first reporting, psutil.cpu_percent() will 
        # return a meaningless value if execute immediately after its importing 
        time.sleep(self.initial_wait)

        while self.alive:
            try:
                self._report_system_info()
            except Exception as ex:
                # unexpected error
                self.logger.errorcf('', -1, ex, 'SystemInfoReporter: unexpected error in _worker_run')

            time.sleep(self.interval)

    
    def _report_system_info(self):
        # cpu
        cpu_percent = psutil.cpu_percent()
        self.logger.event(f'{KEY_PREFIX}CpuUtilization', '', cpu_percent)

        # memory
        memory_percent = psutil.virtual_memory().percent
        self.logger.event(f'{KEY_PREFIX}MemoryUtilization', '', memory_percent)

        # gpu
        # Only for the first time (partial first time) unable to get gpu info, log
        # will be pushed. To avoid frequently being disturbed by cpu error/warn logs.
        gpu_ex = None
        gpu_info = None
        try:
            gpu_info = self._get_gpu_info()
        except Exception as ex:
            gpu_ex = ex

        if gpu_ex:
            # gpu error
            if self.gputil_success:
                self.gputil_success = False
                self.logger.errorcf('', -1, gpu_ex, 'SystemInfoReporter: failed to get gpu info')

        elif gpu_info is None:
            # no gpu
            if self.gputil_success:
                self.gputil_success = False
                self.logger.warnf('SystemInfoReporter: no gpu available')

        else:
            # success
            if not self.gputil_success:
                self.gputil_success = True
            gpu_utilization, gpu_memory_utilization = gpu_info
            self.logger.event(f'{KEY_PREFIX}GpuUtilization', '', gpu_utilization)
            self.logger.event(f'{KEY_PREFIX}GpuMemoryUtilization', '', gpu_memory_utilization)


    def _get_gpu_info(self) -> Optional[Tuple[float, float]]:
        ''' Return (gpu_utilization, gpu_memory_utilization)
            if gpu not available, return None
        '''
        gpus: List[GPUtil.GPU] = GPUtil.getGPUs()
        if not gpus:
            return None

        gpu_utilization = sum(g.load for g in gpus) / len(gpus)
        gpu_memory_utilization = sum(g.memoryUtil for g in gpus) / len(gpus)
        if math.isnan(gpu_utilization) or math.isnan(gpu_memory_utilization):
            raise Exception('gpu utilization or gpu memory utilization is nan')

        return gpu_utilization, gpu_memory_utilization
    
        