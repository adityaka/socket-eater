
import time 
from task_interface import RunTask
from applog import LoggerFactory
class PrintToLogTask(RunTask):
    """Dummy Task to test needs to be removed
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    
    def __init__(self, **kwargs):
        super(PrintToLogTask, self).__init__(**kwargs)
        self._logger = LoggerFactory.get("PrintToLogTask")
    def __call__(self):
        while True:
            self._logger.info("Printing to the log")
            time.sleep(5)
            if self.is_shutdown_triggerred():
                break