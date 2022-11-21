from typing import Union

from telebox.bot.types.types.passport_element_error_data_field import (
    PassportElementErrorDataField
)
from telebox.bot.types.types.passport_element_error_front_side import (
    PassportElementErrorFrontSide
)
from telebox.bot.types.types.passport_element_error_reverse_side import (
    PassportElementErrorReverseSide
)
from telebox.bot.types.types.passport_element_error_selfie import (
    PassportElementErrorSelfie
)
from telebox.bot.types.types.passport_element_error_file import (
    PassportElementErrorFile
)
from telebox.bot.types.types.passport_element_error_files import (
    PassportElementErrorFiles
)
from telebox.bot.types.types.passport_element_error_translation_file import (
    PassportElementErrorTranslationFile
)
from telebox.bot.types.types.passport_element_error_translation_files import (
    PassportElementErrorTranslationFiles
)
from telebox.bot.types.types.passport_element_error_unspecified import (
    PassportElementErrorUnspecified
)


PassportElementError = Union[PassportElementErrorDataField,
                             PassportElementErrorFrontSide,
                             PassportElementErrorReverseSide,
                             PassportElementErrorSelfie,
                             PassportElementErrorFile,
                             PassportElementErrorFiles,
                             PassportElementErrorTranslationFile,
                             PassportElementErrorTranslationFiles,
                             PassportElementErrorUnspecified]
