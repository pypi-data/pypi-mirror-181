"""Responder always answering with 'ok'."""

from . import MockResponder


class OkResponder(MockResponder):
    """
    Responder that always returns 'ok'.
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
            Always 'ok'.
        """
        return 'ok'
