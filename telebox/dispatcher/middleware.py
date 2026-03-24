

class Middleware:
    def on_pre_process(self, ctx) -> None:
        pass

    def on_start(self, ctx) -> dict:
        pass

    def on_process(self, ctx) -> None:
        pass

    def on_post_process(self, ctx) -> None:
        pass

    def on_error(self, ctx) -> None:
        pass

    def on_finish(self, ctx, data: dict) -> None:
        pass
