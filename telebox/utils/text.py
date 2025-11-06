

def get_text_with_surrogates(text: str) -> bytes:
    return text.encode("UTF-16-LE")


def get_text_without_surrogates(text: bytes) -> str:
    return text.decode("UTF-16-LE")
