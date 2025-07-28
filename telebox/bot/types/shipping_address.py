from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class ShippingAddress(Type):
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str
