
from .custom_exception import CustomException


class BadRequestException(CustomException):

    status_code = 400

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def serialize_errors(self):
        return [{"message": self.message}]
