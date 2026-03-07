from telebox.errors import TeleboxError


class StateMachineError(TeleboxError):
    pass


class PreviousStateNotFoundError(StateMachineError):
    pass
