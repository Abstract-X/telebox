MESSAGE = """
    @property
    def chat_type(self) -> str:
        return self.chat.type

    @property
    def chat_id(self) -> int:
        return self.chat.id

    @property
    def unprefixed_chat_id(self) -> int:
        return get_unprefixed_chat_id(self.chat.id, self.chat.type)

    @property
    def user_id(self) -> Optional[int]:
        return self.from_.id if self.from_ else None

    @property
    def sender_chat_id(self) -> Optional[int]:
        return self.sender_chat.id if self.sender_chat else None

    @property
    def unprefixed_sender_chat_id(self) -> Optional[int]:
        if self.sender_chat:
            return get_unprefixed_chat_id(
                chat_id=self.sender_chat.id,
                chat_type=self.sender_chat.type
            )

    @property
    def best_photo(self) -> Optional[PhotoSize]:
        if self.photo:
            return self.photo[-1]

    @property
    def is_forwarded(self) -> bool:
        return bool(self.forward_origin)

    @property
    def is_reply(self) -> bool:
        return bool(self.reply_to_message)

    @property
    def link(self) -> Optional[str]:
        if self.chat.type != "private":
            if self.chat.username:
                return get_message_public_link(self.chat.username, self.message_id)
            else:
                return get_message_private_link(self.unprefixed_chat_id, self.message_id)

    def get_text(self, parse_mode: Optional[str] = None) -> Optional[str]:
        if self.text:
            text = self.text
        elif self.caption:
            text = self.caption
        else:
            return None

        if not text:
            return None

        if parse_mode is None:
            return text

        return get_text_formatter(parse_mode).get_formatted_text(
            text=text,
            entities=self.get_entities()
        )

    def get_entity_text(self, entity: MessageEntity) -> Optional[str]:
        text = self.get_text()

        if text:
            text = get_text_with_surrogates(text)

            return get_text_without_surrogates(text[entity.offset * 2:entity.end_offset * 2])

    def get_entities(self) -> list[MessageEntity]:
        if self.entities:
            return self.entities
        elif self.caption_entities:
            return self.caption_entities

        return []

    def get_command_args(self) -> list[str]:
        text = self.get_text()
        args = []

        if text:
            for i in text.split(" ")[1:]:
                if i:
                    args.append(i)

        return args"""

CALLBACK_QUERY = """
    @property
    def chat_type(self) -> Optional[str]:
        return self.message.chat.type if self.message else None

    @property
    def chat_id(self) -> Optional[int]:
        return self.message.chat.id if self.message else None

    @property
    def unprefixed_chat_id(self) -> Optional[int]:
        if self.chat_id and self.chat_type:
            return get_unprefixed_chat_id(self.chat_id, self.chat_type)

    @property
    def user_id(self) -> int:
        return self.from_.id

    @property
    def message_id(self) -> Optional[int]:
        return self.message.message_id if self.message else None

    @property
    def payload(self) -> Union[str, int, float, bool, list, None]:
        if self.data:
            _, payload = get_parsed_callback_data(self.data)

            return payload"""

MESSAGE_ENTITY = """
    @property
    def end_offset(self) -> int:
        return self.offset + self.length"""

INLINE_KEYBOARD_MARKUP = """
    @property
    def rows(self) -> int:
        return len(self.inline_keyboard)

    def add_row(self, *buttons: InlineKeyboardButton) -> None:
        self.inline_keyboard.append(
            list(buttons)
        )

    def get_row_length(self, *, index: int = -1) -> int:
        return len(self.inline_keyboard[index])

    def add_in_row(self, button: InlineKeyboardButton, *, index: int = -1) -> None:
        self.inline_keyboard[index].append(button)"""

INPUT_CONTACT_MESSAGE_CONTENT = """
    @property
    def full_name(self) -> str:
        return get_full_name(self.first_name, self.last_name)"""

MESSAGE_REACTION_UPDATED = """
    @property
    def chat_type(self) -> str:
        return self.chat.type

    @property
    def chat_id(self) -> int:
        return self.chat.id

    @property
    def unprefixed_chat_id(self) -> int:
        return get_unprefixed_chat_id(self.chat.id, self.chat.type)

    @property
    def user_id(self) -> Optional[int]:
        return self.user.id if self.user else None"""

PRE_CHECKOUT_QUERY = """
    @property
    def user_id(self) -> int:
        return self.from_.id"""

USER = """
    @property
    def full_name(self) -> str:
        return get_full_name(self.first_name, self.last_name)

    @property
    def link(self) -> Optional[str]:
        if self.username:
            return get_username_link(self.username)

    @property
    def mention_link(self) -> str:
        return get_user_link(self.id)"""

SHIPPING_QUERY = """
    @property
    def user_id(self) -> int:
        return self.from_.id"""

CONTACT = """
    @property
    def full_name(self) -> str:
        return get_full_name(self.first_name, self.last_name)"""

CHOSEN_INLINE_RESULT = """
    @property
    def user_id(self) -> int:
        return self.from_.id"""

CHAT = """
    @property
    def full_name(self) -> Optional[str]:
        if self.first_name:
            return get_full_name(self.first_name, self.last_name)

    @property
    def link(self) -> Optional[str]:
        if self.username:
            return get_username_link(self.username)"""

CHAT_FULL_INFO = """
    @property
    def full_name(self) -> Optional[str]:
        if self.first_name:
            return get_full_name(self.first_name, self.last_name)

    @property
    def link(self) -> Optional[str]:
        if self.username:
            return get_username_link(self.username)
        elif self.invite_link:
            return self.invite_link"""

MESSAGE_REACTION_COUNT_UPDATED = """
    @property
    def chat_type(self) -> str:
        return self.chat.type

    @property
    def chat_id(self) -> int:
        return self.chat.id

    @property
    def unprefixed_chat_id(self) -> int:
        return get_unprefixed_chat_id(self.chat.id, self.chat.type)"""

CHAT_JOIN_REQUEST = """
    @property
    def chat_type(self) -> str:
        return self.chat.type

    @property
    def chat_id(self) -> int:
        return self.chat.id

    @property
    def unprefixed_chat_id(self) -> int:
        return get_unprefixed_chat_id(self.chat.id, self.chat.type)

    @property
    def user_id(self) -> int:
        return self.from_.id"""

POLL_ANSWER = """
    @property
    def chat_type(self) -> Optional[str]:
        if self.voter_chat:
            return self.voter_chat.type

    @property
    def chat_id(self) -> Optional[int]:
        if self.voter_chat:
            return self.voter_chat.id

    @property
    def unprefixed_chat_id(self) -> Optional[int]:
        if self.voter_chat:
            return get_unprefixed_chat_id(self.voter_chat.id, self.voter_chat.type)

    @property
    def user_id(self) -> Optional[int]:
        if self.user:
            return self.user.id"""

INLINE_QUERY = """
    @property
    def user_id(self) -> int:
        return self.from_.id"""

REPLY_KEYBOARD_MARKUP = """
    @property
    def rows(self) -> int:
        return len(self.keyboard)

    def add_row(self, *buttons: KeyboardButton) -> None:
        self.keyboard.append(
            list(buttons)
        )

    def get_row_length(self, *, index: int = -1) -> int:
        return len(self.keyboard[index])

    def add_in_row(self, button: KeyboardButton, *, index: int = -1) -> None:
        self.keyboard[index].append(button)"""

CHAT_MEMBER_UPDATED = """
    @property
    def chat_type(self) -> str:
        return self.chat.type

    @property
    def chat_id(self) -> int:
        return self.chat.id

    @property
    def unprefixed_chat_id(self) -> int:
        return get_unprefixed_chat_id(self.chat.id, self.chat.type)

    @property
    def user_id(self) -> int:
        return self.from_.id"""

BUSINESS_CONNECTION = """
    @property
    def user_id(self) -> int:
        return self.user.id"""

BUSINESS_MESSAGES_DELETED = """
    @property
    def chat_type(self) -> str:
        return self.chat.type

    @property
    def chat_id(self) -> int:
        return self.chat.id

    @property
    def unprefixed_chat_id(self) -> int:
        return get_unprefixed_chat_id(self.chat.id, self.chat.type)"""

CHAT_BOOST_REMOVED = """
    @property
    def chat_type(self) -> str:
        return self.chat.type

    @property
    def chat_id(self) -> int:
        return self.chat.id

    @property
    def unprefixed_chat_id(self) -> int:
        return get_unprefixed_chat_id(self.chat.id, self.chat.type)
    
    @property
    def user_id(self) -> Optional[int]:
        if self.source.user:
            return self.source.user.id"""

CHAT_BOOST_UPDATED = """
    @property
    def chat_type(self) -> str:
        return self.chat.type

    @property
    def chat_id(self) -> int:
        return self.chat.id

    @property
    def unprefixed_chat_id(self) -> int:
        return get_unprefixed_chat_id(self.chat.id, self.chat.type)

    @property
    def user_id(self) -> Optional[int]:
        if self.boost.source.user:
            return self.boost.source.user.id"""

PAID_MEDIA_PURCHASED = """
    @property
    def user_id(self) -> int:
        return self.from_.id"""

TYPE_ADDITIONAL_CODES = {
    "Message": MESSAGE,
    "CallbackQuery": CALLBACK_QUERY,
    "MessageEntity": MESSAGE_ENTITY,
    "InlineKeyboardMarkup": INLINE_KEYBOARD_MARKUP,
    "InputContactMessageContent": INPUT_CONTACT_MESSAGE_CONTENT,
    "MessageReactionUpdated": MESSAGE_REACTION_UPDATED,
    "PreCheckoutQuery": PRE_CHECKOUT_QUERY,
    "User": USER,
    "ShippingQuery": SHIPPING_QUERY,
    "Contact": CONTACT,
    "ChosenInlineResult": CHOSEN_INLINE_RESULT,
    "Chat": CHAT,
    "ChatFullInfo": CHAT_FULL_INFO,
    "MessageReactionCountUpdated": MESSAGE_REACTION_COUNT_UPDATED,
    "ChatJoinRequest": CHAT_JOIN_REQUEST,
    "PollAnswer": POLL_ANSWER,
    "InlineQuery": INLINE_QUERY,
    "ReplyKeyboardMarkup": REPLY_KEYBOARD_MARKUP,
    "ChatMemberUpdated": CHAT_MEMBER_UPDATED,
    "BusinessConnection": BUSINESS_CONNECTION,
    "BusinessMessagesDeleted": BUSINESS_MESSAGES_DELETED,
    "ChatBoostRemoved": CHAT_BOOST_REMOVED,
    "ChatBoostUpdated": CHAT_BOOST_UPDATED,
    "PaidMediaPurchased": PAID_MEDIA_PURCHASED
}

TYPE_ADDITIONAL_CODE_IMPORTS = {
    "Message": [
        ("typing", "Optional"),
        ("attrs", "field"),
        ("telebox.bot.utils.ids", "get_unprefixed_chat_id"),
        ("telebox.bot.utils.links", "get_message_public_link"),
        ("telebox.bot.utils.links", "get_message_private_link"),
        ("telebox.bot.utils.utils", "get_text_formatter"),
        ("telebox.utils.text", "get_text_with_surrogates"),
        ("telebox.utils.text", "get_text_without_surrogates")
    ],
    "CallbackQuery": [
        ("typing", "Optional"),
        ("typing", "Union"),
        ("telebox.bot.utils.ids", "get_unprefixed_chat_id"),
        ("telebox.utils.callback_data", "get_parsed_callback_data")
    ],
    "InputContactMessageContent": [
        ("telebox.bot.utils.users", "get_full_name")
    ],
    "MessageReactionUpdated": [
        ("typing", "Optional"),
        ("telebox.bot.utils.ids", "get_unprefixed_chat_id")
    ],
    "User": [
        ("typing", "Optional"),
        ("telebox.bot.utils.users", "get_full_name"),
        ("telebox.bot.utils.links", "get_username_link"),
        ("telebox.bot.utils.links", "get_user_link")
    ],
    "Contact": [
        ("telebox.bot.utils.users", "get_full_name")
    ],
    "Chat": [
        ("typing", "Optional"),
        ("telebox.bot.utils.users", "get_full_name"),
        ("telebox.bot.utils.links", "get_username_link")
    ],
    "ChatFullInfo": [
        ("typing", "Optional"),
        ("telebox.bot.utils.users", "get_full_name"),
        ("telebox.bot.utils.links", "get_username_link")
    ],
    "MessageReactionCountUpdated": [
        ("telebox.bot.utils.ids", "get_unprefixed_chat_id")
    ],
    "ChatJoinRequest": [
        ("telebox.bot.utils.ids", "get_unprefixed_chat_id")
    ],
    "PollAnswer": [
        ("typing", "Optional"),
        ("telebox.bot.utils.ids", "get_unprefixed_chat_id")
    ],
    "ChatMemberUpdated": [
        ("telebox.bot.utils.ids", "get_unprefixed_chat_id")
    ],
    "BusinessMessagesDeleted": [
        ("telebox.bot.utils.ids", "get_unprefixed_chat_id")
    ],
    "ChatBoostRemoved": [
        ("typing", "Optional"),
        ("telebox.bot.utils.ids", "get_unprefixed_chat_id")
    ],
    "ChatBoostUpdated": [
        ("typing", "Optional"),
        ("telebox.bot.utils.ids", "get_unprefixed_chat_id")
    ]
}
