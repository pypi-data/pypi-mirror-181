"""Test the JSON responder class."""

import pytest
from genericserver.responders.json_responder import JsonResponder


@pytest.fixture(autouse=True)
def setup_all(mocker):
    """
    Setup for all tests.

    Parameters
    ----------
    mocker:
        pytest-mock fixture
    """
    mock_exists = mocker.patch('os.path.exists')
    mock_exists.return_value = False
    mock_open = mocker.patch('builtins.open')
    mock_open.return_value = None



def test_json():
    request = 'test'
    expected_response = 'successful'
    myjson = f'{{"test": "{expected_response}"}}'
    print(myjson)
    responder = JsonResponder(myjson)
    response = responder.respondTo(request)
    assert response == expected_response, \
        (f"The JSON responder should return the answer stored in the JSON. "
         f"Request: '{request}', Response: '{response}'")


def test_json_nested():
    request1 = 'test:a'
    expected_response1 = '1'
    request2 = 'test:b'
    expected_response2 = '2'

    myjson = f'{{"test": {{"a": "1", "b": 2}}}}'
    responder = JsonResponder(myjson)

    response1 = responder.respondTo(request1)
    assert response1 == expected_response1, \
        (f"The JSON responder should return the answer stored in the JSON. "
         f"Request: '{request1}', Response: '{expected_response1}'")

    response2 = responder.respondTo(request2)
    assert response2 == expected_response2, \
        (f"The JSON responder should return the answer stored in the JSON. "
         f"Request: '{request2}', Response: '{expected_response2}'")


def test_json_nested_invalid_key():
    request1 = 'test2'
    request2 = 'test:c'
    expected_response = ''

    myjson = f'{{"test": {{"a": "1", "b": 2}}}}'
    responder = JsonResponder(myjson)

    response1 = responder.respondTo(request1)
    assert response1 == expected_response, \
        (f"The JSON responder should return the answer stored in the JSON. "
         f"Request: '{request1}', Response: '{expected_response}'")

    response2 = responder.respondTo(request2)
    assert response2 == expected_response, \
        (f"The JSON responder should return the answer stored in the JSON. "
         f"Request: '{request2}', Response: '{expected_response}'")

def test_json_nested_dot():
    request1 = 'test.a'
    expected_response1 = '1'
    request2 = 'test.b'
    expected_response2 = '2'

    myjson = f'{{"test": {{"a": "1", "b": 2}}}}'
    responder = JsonResponder(myjson, delimiter='.')

    response1 = responder.respondTo(request1)
    assert response1 == expected_response1, \
        (f"The JSON responder should return the answer stored in the JSON. "
         f"Request: '{request1}', Response: '{expected_response1}'")

    response2 = responder.respondTo(request2)
    assert response2 == expected_response2, \
        (f"The JSON responder should return the answer stored in the JSON. "
         f"Request: '{request2}', Response: '{expected_response2}'")


def test_json_nested_from_file(mocker):
    request1 = 'test:a'
    expected_response1 = '1'
    request2 = 'test:b'
    expected_response2 = '2'
    filename = 'test.json'

    # set up mocks
    mock_load = mocker.patch('json.load')
    mock_load.return_value = {'test': {'a': '1',
                                       'b': 2}}
    mock_exists = mocker.patch('os.path.exists')
    mock_exists.return_value = True
    mock_open = mocker.patch('builtins.open')

    responder = JsonResponder(filename)

    response1 = responder.respondTo(request1)
    assert response1 == expected_response1, \
        (f"The JSON responder should return the answer stored in the JSON. "
         f"Request: '{request1}', Response: '{expected_response1}'")

    response2 = responder.respondTo(request2)
    assert response2 == expected_response2, \
        (f"The JSON responder should return the answer stored in the JSON. "
         f"Request: '{request2}', Response: '{expected_response2}'")
