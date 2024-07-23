from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import transaction_partner_types


@dataclass(repr=False)
class TransactionPartnerTelegramAds(Type):
    type: str = transaction_partner_types.TELEGRAM_ADS
