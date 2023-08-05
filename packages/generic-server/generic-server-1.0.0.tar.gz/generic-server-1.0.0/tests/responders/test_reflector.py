"""Tests for the Reflector."""
from genericserver.responders.reflector import Reflector


def test_reflect():
    request = 'test'
    reflector = Reflector()
    response = reflector.respondTo(request)

    assert request == response, \
        f'The reflector should just return the request. Request: {request}, Response: {response}'
