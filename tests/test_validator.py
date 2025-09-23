from validator import Validator


def test_validator():
    v = Validator({"USD", "EUR"})
    assert v.validate({"status": "completed", "amount": "10", "currency": "USD"}) is None
    assert v.validate({"status": "failed", "amount": "10", "currency": "USD"}) == "Invalid status"
    assert v.validate({"status": "completed", "amount": "abc", "currency": "USD"}) == "Invalid amount"
    assert v.validate({"status": "completed", "amount": "10", "currency": "GBP"}) == "Unsupported currency"
