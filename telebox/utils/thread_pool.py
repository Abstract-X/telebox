from threading import Thread, Barrier, Lock
from typing import Callable, Optional, Union, Any


class ThreadPool:

    def __init__(
        self,
        min_threads: int,
        max_threads: int,
        target: Callable,
        *,
        args: tuple = (),
        kwargs: Optional[dict[str, Any]] = None,
        with_barrier: bool = False
    ):
        if min_threads < 1:
            raise ValueError("Number of threads cannot be less than 1!")

        if max_threads < min_threads:
            raise ValueError("Maximum number of threads cannot be less than minimum!")

        self.max_threads = max_threads
        self._target = target
        self._args = args
        self._kwargs = kwargs or {}
        self._threads = [
            Thread(target=self._process, daemon=True)
            for _ in range(min_threads)
        ]
        self._barrier = Barrier(min_threads) if with_barrier else None
        self._lock = Lock()

    @property
    def threads(self) -> int:
        with self._lock:
            return len(self._threads)

    def start_threads(self) -> None:
        with self._lock:
            for i in self._threads:
                i.start()

    def create_thread(self) -> None:
        with self._lock:
            if len(self._threads) == self.max_threads:
                raise RuntimeError("Maximum number of threads has been reached!")

            thread = Thread(target=self._target, args=self._args, kwargs=self._kwargs, daemon=True)
            self._threads.append(thread)
            thread.start()

    def wait_threads(self, timeout_secs: Union[int, float, None] = None) -> None:
        with self._lock:
            for i in self._threads:
                i.join(timeout_secs)

    def _process(self) -> None:
        if self._barrier is not None:
            self._barrier.wait()

        self._target(*self._args, **self._kwargs)
