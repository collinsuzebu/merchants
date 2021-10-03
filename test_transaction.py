import pytest

from .transaction import Transaction


def expected_transaction(value, volume, currency):
    return {"valueTransactions": { "amount" : value, "currency": currency}, "volumeTransactions": volume}


def test_instanstiating_transaction_without_merchantId_raises_error():
    with pytest.raises(Exception) as e_info:
        transaction = Transaction()


def test_can_instanstiate_transaction_without_errors():
    transaction = Transaction("12345")
    assert isinstance(transaction, Transaction)


def test_it_returns_None_for_transactions_with_invalid_merchantId():
    transaction = Transaction("invalid_id_555")
    tr_result = transaction.calculate_transactions()

    assert tr_result == None


def test_it_can_return_other_currencies():
    transaction = Transaction("1234567890", currency="USD")
    tr_result = transaction.calculate_transactions()

    assert tr_result == expected_transaction(259, 3, "USD")


def test_it_properly_calculate_transactions_for_valid_merchantIds():
    transaction_1 = Transaction("1234567890")
    tr_result_1 = transaction_1.calculate_transactions()

    transaction_2 = Transaction("1234567891")
    tr_result_2 = transaction_2.calculate_transactions()

    assert tr_result_1 == expected_transaction(259, 3, "GBP")
    assert tr_result_2 == expected_transaction(99, 1, "GBP")


def test_it_properly_calculate_transactions_for_date_range():
    start_date_1 = "2021-06-20T00:00:00Z"
    end_date_1 = "2021-09-20T00:00:00Z"
    transaction_1 = Transaction("1234567890", start_date_1, end_date_1)
    tr_result_1 = transaction_1.calculate_transactions()

    start_date_2 = "2021-09-20T00:00:00Z"
    end_date_2 = "2021-12-20T00:00:00Z"
    transaction_2 = Transaction("1234567891", start_date_2, end_date_2)
    tr_result_2 = transaction_2.calculate_transactions()

    assert tr_result_1 == expected_transaction(187, 2, "GBP")
    assert tr_result_2 == expected_transaction(0, 0, "GBP")


