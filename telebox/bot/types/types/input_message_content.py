from typing import Union

from telebox.bot.types.types.input_text_message_content import (
    InputTextMessageContent
)
from telebox.bot.types.types.input_location_message_content import (
    InputLocationMessageContent
)
from telebox.bot.types.types.input_venue_message_content import (
    InputVenueMessageContent
)
from telebox.bot.types.types.input_contact_message_content import (
    InputContactMessageContent
)
from telebox.bot.types.types.input_invoice_message_content import (
    InputInvoiceMessageContent
)


InputMessageContent = Union[InputTextMessageContent,
                            InputLocationMessageContent,
                            InputVenueMessageContent,
                            InputContactMessageContent,
                            InputInvoiceMessageContent]
