
from .custom_exception import CustomException


class NotFoundException(CustomException):

    status_code = 400
    message = "Resource Not Found"

    def __init__(self):
        super().__init__("Resource Not Found")

    def serialize_errors(self):
        return [{"message": self.message}]
