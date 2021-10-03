from falcon import testing
import pytest

from .app import app

base_endpoint = "/transactions/all"

def expected_error(merchantId):
    return {"message": "'{0}' not found".format(merchantId)} 

@pytest.fixture(scope='module')
def client():
    return testing.TestClient(app)

def test_can_access_merchant_endpoint(client):
    result = client.simulate_get(base_endpoint + '/1234567890')
    assert result.status_code >= 200

def test_can_get_merchant_transaction_from_resource(client):
    resp = "{'valueTransactions': {'amount': 259, 'currency': 'GBP'}, 'volumeTransactions': 3}"
    result = client.simulate_get(base_endpoint + '/1234567890')

    assert result.status_code == 200
    assert result.text == resp

def test_can_get_merchant_transaction_from_resource_with_date_range(client):
    resp = "{'valueTransactions': {'amount': 97, 'currency': 'GBP'}, 'volumeTransactions': 1}"
    endpoint = base_endpoint + '/1234567890?startDate=2021-06-20T00:00:00Z&endDate=2021-06-20T00:00:00Z'
    result = client.simulate_get(endpoint)

    assert result.status_code == 200
    assert result.text == resp

def test_can_get_merchant_transaction_from_resource_with_other_currencies(client):
    resp = "{'valueTransactions': {'amount': 0, 'currency': 'USD'}, 'volumeTransactions': 0}"
    endpoint = base_endpoint + '/1234567891?currency=USD&startDate=2021-09-20T00:00:00Z&endDate=2021-12-20T00:00:00Z'
    result = client.simulate_get(endpoint)

    assert result.status_code == 200
    assert result.text == resp

def test_it_returns_error_message_when_merchantId_is_invalid(client):
    resp = str(expected_error('invalid_merchant_id'))
    endpoint = base_endpoint + '/invalid_merchant_id'
    result = client.simulate_get(endpoint)

    assert result.status_code == 404
    assert result.text == resp


def test_it_returns_error_message_on_bad_date_request(client):
    resp = str({"message": "an error has occurred"})
    endpoint = base_endpoint + '/1234567891?currency=USD&startDate=2021-09-20T00:00:00Z&endDate=2021-44-20T00:00:00Z'
    result = client.simulate_get(endpoint)

    assert result.status_code == 400
    assert result.text == resp