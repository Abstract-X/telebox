from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass
class ShippingAddress(Type):
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str
