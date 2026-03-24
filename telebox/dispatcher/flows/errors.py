from telebox.errors import TeleboxError


class FlowError(TeleboxError):
    pass


class FlowNotFoundError(FlowError):
    pass
