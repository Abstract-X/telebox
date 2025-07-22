from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User


@define(repr=False)
class ProximityAlertTriggered(Type):
    traveler: User
    watcher: User
    distance: int
