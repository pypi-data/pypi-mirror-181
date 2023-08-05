"""Test okresponder."""
from genericserver.responders.okresponder import OkResponder


def test_response():
    request = 'test'
    responder = OkResponder()
    response = responder.respondTo(request)
    assert response == 'ok',\
        f"Response should always be 'ok'. Request: '{request}, Response: '{response}'"
