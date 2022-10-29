from telebox import State, AbstractEventHandler


class InitialState(State):
    pass


class FooState(State):
    pass


class Handler(AbstractEventHandler):

    def process_event(self, event) -> None:
        pass
