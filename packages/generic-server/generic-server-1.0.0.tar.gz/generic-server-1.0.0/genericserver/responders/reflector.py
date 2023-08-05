""" Responder reflecting a request."""
from . import MockResponder


class Reflector(MockResponder):
    """
    Responder class that reflects the incoming request back to the sender.
    """
    def respondTo(self, request: str) -> str:
        """
        Get response to given request.

        Parameters
        ----------
        request:
            The string to be answered.

        Returns
        -------
            Returns the request as an answer.
        """
        return request
