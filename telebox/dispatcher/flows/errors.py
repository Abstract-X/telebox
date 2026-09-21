from telebox.errors import TeleboxError


class FlowError(TeleboxError):
    pass


class FlowNotFoundError(FlowError):
    pass


class FlowAlreadyExistsError(FlowError):
    pass
