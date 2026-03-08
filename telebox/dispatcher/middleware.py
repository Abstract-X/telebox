from telebox.dispatcher.context import EventContext


class Middleware:
    def pre_process_event(self, ctx: EventContext) -> None:
        pass

    def process_event(self, ctx: EventContext) -> None:
        pass

    def post_process_event(self, ctx: EventContext) -> None:
        pass

    def process_error(self, ctx: EventContext) -> None:
        pass
