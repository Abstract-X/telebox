from telebox.contexts import EventContext


class Middleware:
    def pre_process_event(self, context: EventContext) -> None:
        pass

    def process_event(self, context: EventContext) -> None:
        pass

    def post_process_event(self, context: EventContext) -> None:
        pass

    def process_error(self, context: EventContext) -> None:
        pass
