from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User


@dataclass(repr=False)
class ProximityAlertTriggered(Type):
    traveler: User
    watcher: User
    distance: int
