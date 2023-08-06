from .custom_exception import CustomException


class RequestValidationException(CustomException):

    status_code = 400

    def __init__(self, errors):
        super().__init__('Validation Error')
        self.errors = errors.__dict__["messages"]

    def serialize_errors(self):

        serializedErrors = []
        for field, messages in self.errors.items():

            if isinstance(messages, dict):
                for k, v in messages.items():
                    serializedErrors.append({"message": v[0], "field": field})

            if isinstance(messages, list):
                for msg in messages:
                    serializedErrors.append({"message": msg, "field": field})
        return serializedErrors
