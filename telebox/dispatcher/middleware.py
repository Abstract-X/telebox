from telebox.dispatcher.context import Context


class Middleware:
    def pre_process_event(self, context: Context) -> None:
        pass

    def process_event(self, context: Context) -> None:
        pass

    def post_process_event(self, context: Context) -> None:
        pass

    def process_error(self, context: Context) -> None:
        pass
