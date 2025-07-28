from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import transaction_partner_types


@define(repr=False)
class TransactionPartnerTelegramAds(Type):
    type: str = transaction_partner_types.TELEGRAM_ADS
