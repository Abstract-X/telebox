from typing import Union


class RateLimiter:

    def __init__(self, secs: Union[int, float]):
        if secs <= 0:
            raise ValueError(f"Seconds must be greater than zero!")

        self.secs = float(secs)

    def process(self, event) -> None:
        pass
