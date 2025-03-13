from app.calculation import add, BankAccount
import pytest


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, result", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, result):
    print("testing add function")
    assert add(num1, num2) == result

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit():
    bank_account = BankAccount(50)
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_collect_interest():
    bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance) == 55

def test_bank_transaction(zero_bank_account):
    zero_bank_account.deposit(200)
    zero_bank_account.withdraw(100)
    assert zero_bank_account.balance == 100

@pytest.mark.parametrize("deposited, withdraw, expected", [
    (300, 200, 100),
    (700, 100, 600),
    (1200, 400, 800)
])
def test_bank_transaction(zero_bank_account, deposited, withdraw, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(200)