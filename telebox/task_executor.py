import logging
from typing import Callable, Any, Optional, Union
from dataclasses import dataclass
import threading
from threading import Thread, RLock, Condition
import heapq
import time
import uuid


logger = logging.getLogger(__name__)
_WORKER_WAITING_SECS = 60


@dataclass
class Task:
    id: str
    task: Callable
    args: tuple
    kwargs: dict[str, Any]
    start_time: float
    is_cancelled: bool = False


class TaskExecutor:
    def __init__(self, min_workers: int = 10, max_workers: int = 100):
        self._min_workers = min_workers
        self._max_workers = max_workers
        self._workers: dict[str, Thread] = {}
        self._worker_lock = RLock()
        self._worker_count = 0
        self._tasks: dict[str, Task] = {}
        self._tasks_in_processing = 0
        self._task_heap: list[tuple[float, str]] = []
        self._unprocessed_tasks = 0
        self._task_lock = RLock()
        self._new_task_condition = Condition(self._task_lock)
        self._all_tasks_done_condition = Condition(self._task_lock)
        self._is_started = False

    def __enter__(self) -> "TaskExecutor":
        self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wait()

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

        if not self._is_started:
            raise RuntimeError("Task executor is not started!")

        task = Task(
            id=str(uuid.uuid4()),
            task=task,
            args=args,
            kwargs=kwargs or {},
            start_time=time.monotonic() + delay_secs
        )

        with self._new_task_condition:
            self._tasks[task.id] = task
            heapq.heappush(self._task_heap, (task.start_time, task.id))
            self._unprocessed_tasks += 1
            self._new_task_condition.notify()

        logger.debug("Task added: %r, delay_secs=%r.", task, delay_secs)

        return task.id

    def cancel_task(self, id_: str) -> bool:
        with self._all_tasks_done_condition:
            try:
                task = self._tasks[id_]
            except KeyError:
                return False

            task.is_cancelled = True
            self._unprocessed_tasks -= 1

            if not self._unprocessed_tasks:
                self._all_tasks_done_condition.notify_all()

        logger.debug("Task cancelled: %r.", task)

        return True

    def start(self) -> None:
        if self._is_started:
            raise RuntimeError("Task executor has already been started!")

        self._is_started = True

        with self._worker_lock:
            for _ in range(self._min_workers):
                self._create_worker()

        logger.info("Tasks started.")

    def wait(self) -> None:
        with self._all_tasks_done_condition:
            while self._unprocessed_tasks:
                self._all_tasks_done_condition.wait()

        logger.info("Tasks finished.")

    def _create_worker(self) -> None:
        self._worker_count += 1
        worker = Thread(
            target=self._run_task_processing,
            name=f"TaskExecutorWorker-{self._worker_count}",
            daemon=True
        )
        self._workers[worker.name] = worker
        logger.debug(
            "Worker %r started (workers: %r).",
            worker.name,
            len(self._workers)
        )
        worker.start()

    def _run_task_processing(self) -> None:
        worker_name = threading.current_thread().name
        last_processing_time = time.monotonic()

        while True:
            with self._new_task_condition:
                while not self._task_heap:
                    remaining_secs = (
                        _WORKER_WAITING_SECS
                        - (time.monotonic() - last_processing_time)
                    )

                    if remaining_secs <= 0:
                        with self._worker_lock:
                            if len(self._workers) > self._min_workers:
                                del self._workers[worker_name]
                                logger.debug(
                                    "Worker %r stopped (workers: %r).",
                                    worker_name,
                                    len(self._workers)
                                )

                                return
                            else:
                                remaining_secs = _WORKER_WAITING_SECS

                    self._new_task_condition.wait(timeout=remaining_secs)

                task_start_time, task_id = self._task_heap[0]
                now_secs = time.monotonic()

                if task_start_time > now_secs:
                    delay_secs = task_start_time - now_secs
                    self._new_task_condition.wait(timeout=delay_secs)
                    continue

                heapq.heappop(self._task_heap)
                task = self._tasks.pop(task_id)

                if task.is_cancelled:
                    continue

                self._tasks_in_processing += 1

                with self._worker_lock:
                    if (
                        (self._tasks_in_processing == len(self._workers))
                        and (len(self._workers) < self._max_workers)
                    ):
                        self._create_worker()

            logger.debug("Task processing started: %r.", task)

            # noinspection PyBroadException
            try:
                task.task(*task.args, **task.kwargs)
            except Exception:
                logger.exception("An error occurred while processing a task!")
            finally:
                self._set_task_completion()
                logger.debug("Task processing finished: %r.", task)

    def _set_task_completion(self) -> None:
        with self._all_tasks_done_condition:
            self._tasks_in_processing -= 1
            self._unprocessed_tasks -= 1

            if not self._unprocessed_tasks:
                self._all_tasks_done_condition.notify_all()
