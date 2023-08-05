from contextlib import contextmanager
from typing import ContextManager
from unittest.mock import Mock, patch


@contextmanager
def mock_cloudinary_upload() -> ContextManager[Mock]:
    with patch("cloudinary.uploader.upload") as mock:
        yield mock


@contextmanager
def mock_cloudinary_delete() -> ContextManager[Mock]:
    with patch("cloudinary.api.delete_resources") as mock:
        yield mock
