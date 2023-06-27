from task_interface import RunTask
from applog import LoggerFactory
import time

import socket
class DnsClientTask(RunTask):
    def __init__(self, domainname):
        self._domainname = domainname
        self._logger = LoggerFactory.get("DnsClientTask")
        super().__init__()
    
    def __call__(self):
        while not self.shutdown_event.is_set():
            self._logger.info("resolving {}".format(self._domainname))
            d = socket.gethostbyname(self._domainname)
            self._logger.debug("Resolved the {} to {}".format(self._domainname, d))
            time.sleep(5)


    