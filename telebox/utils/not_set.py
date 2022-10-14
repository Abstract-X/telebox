

class NotSet:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __repr__(self):
        return type(self).__name__

    def __bool__(self):
        return False
