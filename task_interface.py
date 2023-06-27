from abc import ABCMeta, abstractmethod
import threading

class RunTask(metaclass=ABCMeta):
    
    def __init__(self, **kwargs) -> None:
        self._kwargs = kwargs
        self.shutdown_event = threading.Event()

    @abstractmethod
    def __call__(self) -> None:
        pass 

    def is_shutdown_triggerred(self) -> bool:
        return self.shutdown_event.is_set()
    
    def shutdown(self):
        # don't re-acquire and set the event once it's set
        if self.shutdown_event.is_set():
            return
        self.shutdown_event.set()