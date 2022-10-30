import logging
from typing import Callable, Any, Optional, NoReturn
from dataclasses import dataclass
from queue import Queue

from telebox.utils.thread_pool import ThreadPool


logger = logging.getLogger(__name__)


@dataclass
class Task:
    task: Callable
    args: tuple
    kwargs: dict[str, Any]


class TaskExecutor:

    def __init__(self, threads: int):
        self._thread_pool = ThreadPool(threads, self._run_task_processing)
        self._tasks = Queue()

    def add_task(
        self,
        task: Callable,
        args: tuple = (),
        kwargs: Optional[dict[str, Any]] = None
    ) -> None:
        task = Task(
            task=task,
            args=args,
            kwargs=kwargs or {}
        )
        logger.debug("Task added to queue: %r.", task)
        self._tasks.put(task, block=False)

    def run_tasks(self) -> None:
        logger.debug("Tasks is starting...")
        self._thread_pool.start()
        logger.info("Tasks started.")

    def wait_tasks(self) -> None:
        logger.info("Finishing tasks...")
        self._tasks.join()
        logger.info("Tasks finished.")

    def _run_task_processing(self) -> NoReturn:
        while True:
            task = self._tasks.get()

            # noinspection PyBroadException
            try:
                logger.debug("Task processing started: %r.", task)
                task.task(*task.args, **task.kwargs)
            except Exception:
                logger.exception("An error occurred while processing a task!")
            finally:
                self._tasks.task_done()
                logger.debug("Task processing finished: %r.", task)
