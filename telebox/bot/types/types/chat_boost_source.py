from typing import Union

from telebox.bot.types.types.chat_boost_source_premium import ChatBoostSourcePremium
from telebox.bot.types.types.chat_boost_source_gift_code import ChatBoostSourceGiftCode
from telebox.bot.types.types.chat_boost_source_giveaway import ChatBoostSourceGiveaway


ChatBoostSource = Union[ChatBoostSourcePremium,
                        ChatBoostSourceGiftCode,
                        ChatBoostSourceGiveaway]
