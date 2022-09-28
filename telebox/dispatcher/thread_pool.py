from threading import Thread, Barrier
from typing import Callable


class ThreadPool:

    def __init__(self, threads: int, target: Callable, args: tuple):
        if threads < 1:
            raise ValueError("Number of threads cannot be less than 1!")

        self._target = target
        self._args = args
        self._threads = [
            Thread(target=self._process, daemon=True)
            for _ in range(threads)
        ]
        self._barrier = Barrier(threads)

    def start(self) -> None:
        for i in self._threads:
            i.start()

    def _process(self) -> None:
        self._barrier.wait()
        self._target(*self._args)
