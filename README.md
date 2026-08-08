# Bank Account Unit Testing Project

A Python-based Bank Account project created to demonstrate practical **unit testing, exception handling, mocking, transaction logging, test fixtures, and code coverage**.

## Project Overview

This project implements a simple `BankAccount` class with common banking operations and a comprehensive unit-test suite.

The project was developed as a hands-on exercise to understand how unit testing can be applied to a small object-oriented Python application.

## Features

The `BankAccount` class supports:

- Creating a bank account
- Initial balance validation
- Depositing money using `credit()`
- Withdrawing money using `debit()`
- UPI-style transfers between accounts
- Checking the current balance
- Applying simple interest
- Maintaining transaction history
- Sending transfer notifications
- Object representation using `__repr__()`

## Project Structure

```text
bank-account-unit-testing/
│
├── main.py
├── test_main.py
├── README.md
└── .gitignore
```

## Application Components

### `BankAccount`

The main class represents a bank account and contains the following methods:

| Method | Purpose |
|---|---|
| `credit()` | Deposits money into the account |
| `debit()` | Withdraws money from the account |
| `upi_transfer()` | Transfers money between two accounts |
| `get_balance()` | Returns the current balance |
| `apply_interest()` | Applies simple interest |
| `get_transaction_history()` | Returns transaction history |
| `__repr__()` | Returns a readable account representation |

### `NotificationService`

A small notification service is included to demonstrate dependency injection and mocking during testing.

## Exception Handling

Two custom exceptions are implemented.

### `InvalidAmountError`

This exception is raised when an invalid amount is supplied, including:

- Negative initial balance
- Zero or negative credit amount
- Zero or negative debit amount
- Zero or negative transfer amount
- Negative interest rate

### `InsufficientBalanceError`

This exception is raised when an account does not have sufficient funds for:

- A debit operation
- A UPI transfer

## Unit Testing

The project uses Python's built-in `unittest` framework.

The test suite covers:

- Successful credit operation
- Invalid credit amounts
- Successful debit operation
- Debit with insufficient balance
- Successful UPI transfer
- UPI transfer with insufficient balance
- UPI transfer with an invalid account type
- Balance retrieval
- Interest calculation with multiple rates
- Negative interest validation
- Transaction history
- Notification service mocking
- Negative initial balance
- Invalid debit amounts
- Invalid transfer amounts
- `__repr__()` output

## Test Fixtures

The test class demonstrates the use of different `unittest` lifecycle methods.

### `setUpClass()`

Runs once before the complete test class starts.

### `tearDownClass()`

Runs once after all tests in the class finish.

### `setUp()`

Runs before every test method and creates fresh bank accounts so that tests do not interfere with each other.

### `tearDown()`

Runs after every test method.

## Subtests

`subTest()` is used where multiple related inputs need to be tested independently.

For example:

```python
for bad_amount in [0, -50]:
    with self.subTest(amount=bad_amount):
        with self.assertRaises(InvalidAmountError):
            self.account_a.credit(bad_amount)
```

This makes it easier to identify which input failed if one test case does not behave as expected.

## Mocking

`unittest.mock.Mock` is used to replace the real notification service during testing.

Example:

```python
mock_notifier = Mock()

sender = BankAccount(
    "Alice",
    1000,
    notifier=mock_notifier
)

receiver = BankAccount("Bob", 500)

sender.upi_transfer(receiver, 200)

mock_notifier.send_notification.assert_called_once_with(
    "200 transferred from Alice to Bob"
)
```

This verifies that the notification method was called correctly without relying on an actual external notification system.

## Transaction Logging

Each account maintains an internal transaction history.

Transactions such as:

- Account creation
- Credit
- Debit
- UPI transfer
- UPI receipt
- Interest application

are recorded with timestamps.

The test suite verifies that expected transaction messages are present in the history.

## Running the Tests

Make sure Python is installed and run the following command from the project directory:

```bash
python -m unittest test_main.py -v
```

Alternatively:

```bash
python test_main.py
```

## Code Coverage

The project can be checked using the `coverage` package.

Install it with:

```bash
pip install coverage
```

Run the tests with coverage:

```bash
coverage run -m unittest test_main.py
```

View the coverage summary:

```bash
coverage report
```

For a detailed HTML report:

```bash
coverage html
```

This generates an `htmlcov` directory containing an interactive coverage report.

> **Note:** The coverage percentage should be reported based on the result obtained when running the recreated project locally.

## Technologies Used

- **Python**
- **unittest**
- **unittest.mock**
- **coverage**
- Object-Oriented Programming
- Exception Handling

## Learning Objectives

This project demonstrates practical understanding of:

1. Writing unit tests for Python classes
2. Testing both positive and negative scenarios
3. Custom exception handling
4. Test setup and teardown
5. Using `subTest()` for multiple test cases
6. Mocking dependencies
7. Verifying method calls with mocks
8. Testing object state and return values
9. Maintaining transaction logs
10. Measuring code coverage

## Future Improvements

Possible extensions to the project include:

- Adding account numbers
- Adding transaction IDs
- Supporting multiple account types
- Adding transaction timestamps in a structured format
- Adding persistent storage
- Adding more advanced transaction validation
- Creating a REST API around the bank account functionality

## Author

Personal Python Unit Testing Project
