import logging
from typing import Callable, Any, Optional, Union, NoReturn
from dataclasses import dataclass
from threading import Thread, Lock
from queue import Queue
import time
import uuid

from telebox.utils.thread_pool import ThreadPool
from telebox.utils.task_executor.errors import TaskExecutorError, PendingTaskNotFoundError


logger = logging.getLogger(__name__)
_PENDING_TASK_PROCESSING_DELAY_SECS = 0.1
_TASK_WAITING_DELAY_SECS = 0.1


@dataclass
class Task:
    id: str
    task: Callable
    args: tuple
    kwargs: dict[str, Any]


class TaskExecutor:

    def __init__(self, threads: int, *, allow_pending_tasks: bool = False):
        self._thread_pool = ThreadPool(threads, self._run_task_processing, with_barrier=True)
        self._allow_pending_tasks = allow_pending_tasks
        self._pending_task_processing_thread: Optional[Thread] = None
        self._tasks = Queue()
        self._pending_tasks: list[tuple[Task, float]] = []
        self._pending_task_lock = Lock()

    def __enter__(self):
        self.start_tasks()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wait_tasks()

    def add_task(
        self,
        task: Callable,
        delay_secs: Union[int, float, None] = None,
        args: tuple = (),
        kwargs: Optional[dict[str, Any]] = None
    ) -> str:
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            task=task,
            args=args,
            kwargs=kwargs or {}
        )

        if delay_secs is not None:
            if not self._allow_pending_tasks:
                raise TaskExecutorError("Pending tasks are not allowed!")

            if delay_secs < 0:
                raise ValueError("Delay seconds cannot be negative!")

            with self._pending_task_lock:
                logger.debug("Pending task added to queue: %r, delay_secs=%r.", task, delay_secs)
                self._pending_tasks.append((task, time.monotonic() + delay_secs))
                self._pending_tasks.sort(key=lambda i: i[1], reverse=True)
        else:
            logger.debug("Task added to queue: %r.", task)
            self._tasks.put(task, block=False)

        return task_id

    def remove_pending_task(self, id_: str) -> None:
        with self._pending_task_lock:
            for index, task_items in enumerate(self._pending_tasks):
                if task_items[0].id == id_:
                    self._pending_tasks.pop(index)
                    break
            else:
                raise PendingTaskNotFoundError("Pending task with ID {id!r} not found!", id=id_)

    def start_tasks(self) -> None:
        logger.debug("Tasks is starting...")

        if self._allow_pending_tasks:
            self._pending_task_processing_thread = Thread(
                target=self._run_pending_task_processing,
                daemon=True
            )
            self._pending_task_processing_thread.start()

        self._thread_pool.start()
        logger.info("Tasks started.")

    def wait_tasks(self) -> None:
        logger.info("Finishing tasks...")

        if self._allow_pending_tasks:
            while self._pending_tasks:
                time.sleep(_TASK_WAITING_DELAY_SECS)

            self._pending_task_processing_thread = None

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

    def _run_pending_task_processing(self) -> NoReturn:
        while True:
            with self._pending_task_lock:
                if self._pending_tasks and (time.monotonic() > self._pending_tasks[-1][1]):
                    task, _ = self._pending_tasks.pop()
                    self._tasks.put(task, block=False)
                    continue

            time.sleep(_PENDING_TASK_PROCESSING_DELAY_SECS)
