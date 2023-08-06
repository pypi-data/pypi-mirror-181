import pathlib
from io import BytesIO, IOBase
from typing import Optional
from uuid import uuid4

from PIL import Image

from baseten.common.api import upload_user_file

DEFAULT_FILE_PATH = "png"


def upload_to_s3(io_stream: IOBase, file_name: str) -> str:
    """
    Uploads any stream to S3.

    Args:
        io_stream (IO): Any IO byte stream. This could be a bytes buffer, or
        an open binary file.
        file_name (str): The file_name to use when saving the file to S3

    Returns:
        str: A URL to fetch the uploaded S3 object.
    """

    return upload_user_file(io_stream, file_name)


def upload_pil_to_s3(image: Image, file_name: Optional[str] = None) -> str:
    """
    Uploads a PIL image object to S3.

    Args:
        image (PIL.Image): A PIL image object.
        file_name (Optional[str]): The file_name to use when saving the file to S3.
            Must have an image file extension (.jpg, .png, etc.). Can be None.

    Returns:
        str: A URL to fetch the uploaded S3 object.
    """

    # If no file_name is passed, generate a random file path
    if file_name is None:
        file_name = f"{str(uuid4())}.{DEFAULT_FILE_PATH}"

    # Get the file extension from the passed in file name.
    image_format = pathlib.Path(file_name).suffix.strip(".")

    byte_buffer = BytesIO()
    image.save(byte_buffer, format=image_format)

    return upload_to_s3(byte_buffer, file_name)
