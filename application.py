import signal
import logging
import threading
import argparse
from typing import List
from applog import LoggerFactory
from task_interface import RunTask

class Application(object):
    def __init__(self, logger : logging.Logger, tasks: List[RunTask], parser: argparse.ArgumentParser = None) -> None:
        self._logger = logger
        self._parser = parser
        self._shutdown_signals = [signal.SIGTERM, signal.SIGABRT, signal.SIGSEGV]
        self._task_threads = list()
        self._shutdown_event = threading.Event()
       
        for signum in self._shutdown_signals:
            signal.signal(signum, self.shutdown_signal_handler)
        self._shutdown_thread = threading.Thread(name="shutdown_thread", target=self.wait_for_shutdown, daemon=True)
        #self._task_thread = threading.Thread(name="Task thread", target=self.run_task, daemon=True)
        if len(tasks) == 0:
            raise ValueError("Nothing to do tasklist is empty")
        self._tasks = tasks
        for t in tasks:
            if isinstance(t, RunTask):
                thread = threading.Thread(name="TaskThread", target=t, daemon=True)
                self._task_threads.append(thread)
            else:
                raise ValueError("Application tasks should inherit RunTask")
        
    def shutdown_signal_handler(self, signum, frame) -> None:
        if signum in self._shutdown_signals:
            self._logger.info("signum {} {} received shutting down".format(str(signum), signal.strsignal(signum)))
            self._shutdown_event.set()

    def run_tasks(self) -> None:
        self._logger.info("Starting all task threads")
        for t in self._task_threads:
            t.start()
  
    def wait_for_shutdown(self) -> None:
        self._logger.info("Wait to be shutdown")
        self._shutdown_event.wait()
        self._logger.info("shutdown triggered exitting with success")
        exit(0)

    def __call__(self):
        self._shutdown_thread.start()
        self.run_tasks()
        try:
            self._shutdown_thread.join()
        except KeyboardInterrupt as ke:
            self._logger.info("got CTRL+C shutting down")
            if self._shutdown_event.is_set():
                return
            self._shutdown_event.set()
        finally:
            for t in self._tasks:
                t.shutdown()