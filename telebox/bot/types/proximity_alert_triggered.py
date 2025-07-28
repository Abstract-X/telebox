from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.user import User


@define(repr=False)
class ProximityAlertTriggered(Type):
    traveler: User
    watcher: User
    distance: int
