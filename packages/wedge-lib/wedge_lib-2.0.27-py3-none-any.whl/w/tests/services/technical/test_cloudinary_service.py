from io import BytesIO

from cloudinary import CloudinaryImage

from w.services.technical.cloudinary_service import CloudinaryService
from w.tests.helpers.cloudinary_test_helper import (
    mock_cloudinary_upload,
    mock_cloudinary_delete,
)
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestCloudinaryService(TestCaseMixin):
    service = CloudinaryService

    @classmethod
    def setup_class(cls):
        cls.service.init(cloud_name="TEST", api_key="TEST", api_secret="TEST")

    @classmethod
    def teardown_class(cls):
        cls.service.clear()

    """
    upload
    """

    def test_upload_with_success_return_none(self):
        with mock_cloudinary_upload() as mock:
            self.service.upload("random/file/path")

        assert mock.call_count == 1

    """
    delete
    """

    def test_delete_with_success_return_none(self):
        with mock_cloudinary_delete() as mock:
            self.service.delete("some_public_id1", "some_public_id2")

        assert mock.call_count == 1

    def test_delete_with_no_public_id_return_none(self):
        with mock_cloudinary_delete() as mock:
            self.service.delete()

        assert mock.call_count == 0

    """
    upload_temporary_file
    """

    def test_upload_temporary_file_with_success_return_cloudinary_image(self):
        some_file_bytes = BytesIO()
        some_folder = "cloudinary_folder"
        with mock_cloudinary_upload() as upload_mock:
            with mock_cloudinary_delete() as delete_mock:
                with self.service.upload_temporary_file(
                    some_file_bytes,
                    folder=some_folder,
                ) as image:
                    assert isinstance(image, CloudinaryImage)
                    assert some_folder in str(image)

        assert upload_mock.call_count == delete_mock.call_count == 1
