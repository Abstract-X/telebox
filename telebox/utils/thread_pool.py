from threading import Thread, Barrier
from typing import Callable, Optional, Union, Any


class ThreadPool:

    def __init__(
        self,
        threads: int,
        target: Callable,
        *,
        args: tuple = (),
        kwargs: Optional[dict[str, Any]] = None,
        with_barrier: bool = False
    ):
        if threads < 1:
            raise ValueError("Number of threads cannot be less than 1!")

        self._target = target
        self._args = args
        self._kwargs = kwargs or {}
        self._threads = [
            Thread(target=self._process, daemon=True)
            for _ in range(threads)
        ]
        self._barrier = Barrier(threads) if with_barrier else None

    def start(self) -> None:
        for i in self._threads:
            i.start()

    def wait(self, timeout_secs: Union[int, float, None] = None) -> None:
        for i in self._threads:
            i.join(timeout_secs)

    def _process(self) -> None:
        if self._barrier is not None:
            self._barrier.wait()

        self._target(*self._args, **self._kwargs)
