from base64 import b64encode
from io import BytesIO
from PIL import Image


def bytes2base64(bs: bytes) -> str:
    """Convert byte buffer to base64 string"""
    b64 = b64encode(bs)
    return b64.decode("utf-8")


def bytes2pillow(bs: bytes) -> Image:
    """
    Convert byte buffer to Pillow Image

    Args:
        bs: The byte buffer

    Returns:
        image: A PIL Image
    """
    io = BytesIO(bs)
    image = Image.open(io)
    image.load()
    io.close()
    return image


def pillow2bytes(image: Image) -> bytes:
    """Returns an in-memory byte buffers representing the pillow image file.

    Args:
        image:
            Pillow image to be converted

    Returns:
        buffer:
            Bytes of saved Pillow image
    """
    io = BytesIO()
    image.save(io, "PNG")
    buffer = io.getvalue()
    io.close()
    return buffer


def pillow2base64(image: Image) -> str:
    """Chaining pillow2bytes and bytes2base64"""
    return bytes2base64(pillow2bytes(image))
