import pytest
from app.calculations import add,BankAccount
@pytest.mark.parametrize("num1,num2,expected", [
    (5, 3, 8),
    (10, 2, 12),
    (-1, 1, 0)
])
def test_add(num1, num2, expected):
    sum = add(num1, num2)
    assert sum == expected

def test_bank_set_initial_amount():
    account = BankAccount(100)
    assert account.balance == 100