from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.consts import transaction_partner_types


@define(repr=False)
class TransactionPartnerOther(Type):
    type: str = transaction_partner_types.OTHER
