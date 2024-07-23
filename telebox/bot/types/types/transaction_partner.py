from typing import Union

from telebox.bot.types.types.transaction_partner_user import TransactionPartnerUser
from telebox.bot.types.types.transaction_partner_fragment import TransactionPartnerFragment
from telebox.bot.types.types.transaction_partner_telegram_ads import TransactionPartnerTelegramAds
from telebox.bot.types.types.transaction_partner_other import TransactionPartnerOther


TransactionPartner = Union[TransactionPartnerUser,
                           TransactionPartnerFragment,
                           TransactionPartnerTelegramAds,
                           TransactionPartnerOther]
