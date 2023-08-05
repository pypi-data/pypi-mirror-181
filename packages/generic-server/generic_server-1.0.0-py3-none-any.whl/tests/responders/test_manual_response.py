"""Test ManualResponder."""
from genericserver.responders.manual import ManualResponder


def test_reflect(mocker):
    manual_response = '42'
    mock_input = mocker.patch('builtins.input')
    mock_input.return_value = manual_response

    request = 'test'
    reflector = ManualResponder()
    response = reflector.respondTo(request)
    assert manual_response == response, \
        (f"The manual responder should return the answer entered by the user. "
         f"Request: '{request}', Response: '{response}'")
