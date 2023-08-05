"""Responders for the MockServer."""

from abc import ABC
from abc import abstractmethod


class MockResponder(ABC):
    """
    Abstract Base Class for responders.
    """
    def __int__(self):
        pass

    @abstractmethod
    def respondTo(self, request: str):
        """
        Respond to a given request.
        Parameters
        ----------
        request:
            The request to be answered.
        """
        pass
