import logging
from typing import Callable, Any, Optional, Union, NoReturn
from dataclasses import dataclass
from threading import Thread, Lock, Condition
from queue import SimpleQueue
import time
import uuid

from telebox.utils.thread_pool import ThreadPool
from telebox.utils.task_executor.errors import TaskNotFoundError


logger = logging.getLogger(__name__)


@dataclass
class Task:
    id: str
    task: Callable
    args: tuple
    kwargs: dict[str, Any]
    start_time: float


class TaskExecutor:

    def __init__(self, min_threads: int = 5, max_threads: int = 25):
        self._tasks = []
        self._active_tasks = SimpleQueue()
        self._unfinished_tasks = 0
        self._task_lock = Lock()
        self._all_tasks_done_condition = Condition(self._task_lock)
        self._thread_pool = ThreadPool(
            min_threads,
            max_threads,
            target=self._process_tasks,
            with_barrier=True
        )
        self._busy_threads = 0
        self._busy_thread_lock = Lock()
        self._submission_thread: Optional[Thread] = None

    def __enter__(self):
        self.start_tasks()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wait_tasks()

    def add_task(
        self,
        task: Callable,
        args: tuple = (),
        kwargs: Optional[dict[str, Any]] = None,
        *,
        delay_secs: Union[int, float] = 0
    ) -> str:
        if delay_secs < 0:
            raise ValueError("Delay seconds cannot be negative!")

        task = Task(
            id=str(uuid.uuid4()),
            task=task,
            args=args,
            kwargs=kwargs or {},
            start_time=time.monotonic() + delay_secs
        )

        with self._task_lock:
            for index, i in enumerate(self._tasks):
                if task.start_time > i.start_time:
                    self._tasks.insert(index, task)
                    break
            else:
                self._tasks.append(task)

            self._unfinished_tasks += 1

        logger.debug("Task added to queue: %r, delay_secs=%r.", task, delay_secs)

        return task.id

    def remove_task(self, id_: str) -> None:
        with self._all_tasks_done_condition:
            for index, i in enumerate(self._tasks):
                if i.id == id_:
                    del self._tasks[index]
                    self._unfinished_tasks -= 1
                    logger.debug("Task removed from queue: %r.", i)

                    if not self._unfinished_tasks:
                        self._all_tasks_done_condition.notify_all()

                    break
            else:
                raise TaskNotFoundError("Task with ID {id!r} not found!", id=id_)

    def start_tasks(self) -> None:
        logger.debug("Tasks is starting...")
        self._submission_thread = Thread(target=self._process_task_submission, daemon=True)
        self._submission_thread.start()
        self._thread_pool.start_threads()
        logger.info("Tasks started.")

    def wait_tasks(self) -> None:
        logger.info("Finishing tasks...")

        with self._all_tasks_done_condition:
            while self._unfinished_tasks:
                self._all_tasks_done_condition.wait()

            self._submission_thread = None

        logger.info("Tasks finished.")

    def _process_tasks(self) -> NoReturn:
        while True:
            task = self._active_tasks.get()

            with self._busy_thread_lock:
                self._busy_threads += 1

                if (
                    (self._busy_threads == self._thread_pool.threads)
                    and (self._thread_pool.threads < self._thread_pool.max_threads)
                ):
                    self._thread_pool.create_thread()
                    logger.debug("Additional task processing thread created.")

            # noinspection PyBroadException
            try:
                logger.debug("Task processing started: %r.", task)
                task.task(*task.args, **task.kwargs)
            except Exception:
                logger.exception("An error occurred while processing a task!")
            finally:
                self._set_task_completion()
                logger.debug("Task processing finished: %r.", task)

                with self._busy_thread_lock:
                    self._busy_threads -= 1

    def _process_task_submission(self) -> None:
        while True:
            with self._task_lock:
                while self._tasks and (time.monotonic() > self._tasks[0].start_time):
                    task = self._tasks.pop()
                    self._active_tasks.put(task)

            time.sleep(0.1)

    def _set_task_completion(self) -> None:
        with self._all_tasks_done_condition:
            self._unfinished_tasks -= 1

            if not self._unfinished_tasks:
                self._all_tasks_done_condition.notify_all()
