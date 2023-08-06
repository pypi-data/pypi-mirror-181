from abc import ABC, abstractmethod
from werkzeug.exceptions import HTTPException
import typing as t

# TODO figureout t.NotRequired[str]
serialize_error = t.TypedDict("serialize_error", {
    'message': str,
    'field': t.Optional[str]
})


class CustomException(ABC, HTTPException):

    def __init__(self, message):
        HTTPException.__init__(self, message)

    @property
    @abstractmethod
    def status_code(self) -> None:
        pass

    @abstractmethod
    def serialize_errors(self) -> t.List[serialize_error]:
        pass
