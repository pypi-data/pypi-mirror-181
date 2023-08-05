"""Responder taking answers from a JSON document."""
import os

from . import MockResponder
import json


class JsonResponder(MockResponder):
    """
    Responder that chooses answers from a JSON document.
    """

    def __init__(self, lookup, delimiter=':'):
        if os.path.exists(lookup):
            with open(lookup) as f:
                self._lookup = json.load(f)
        else:
            self._lookup = json.loads(lookup)

        self._delimiter = delimiter

    def _getAnswer(self, breadcrumbs: list[str], lookup: dict):
        """
        Recursive function getting the value from a lookup dictionary.

        Parameters
        ----------
        breadcrumbs:
            List of keywords.
        lookup:
            The lookup dictionary to use.

        Returns
        -------
            Gets the value from a nested dictionary.
        """
        if len(breadcrumbs) == 1:
            return lookup[breadcrumbs[0]]
        else:
            return self._getAnswer(breadcrumbs[1:], lookup[breadcrumbs[0]])

    def respondTo(self, request: str) -> str:
        """
        Get response to given request.

        Parameters
        ----------
        request:
            The string to be answered.

        Returns
        -------
            String representation of the value from the lookup dictionary.
        """
        breadcrumbs = request.split(self._delimiter)
        try:
            response = str(self._getAnswer(breadcrumbs, self._lookup))
        except KeyError:
            print(f"Warning: '{request}' does not exist.")
            response = ''
        return response
