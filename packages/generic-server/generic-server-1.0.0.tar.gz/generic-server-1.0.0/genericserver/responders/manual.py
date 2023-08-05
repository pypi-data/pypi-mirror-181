"""Responder waiting for a manual entry as a response."""

from . import MockResponder


class ManualResponder(MockResponder):
    """
    Responder that waits for a manual answer to a request.
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
            The response manually given by the user.
        """
        return input(f"Please enter response to request '{request}': ")
