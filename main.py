from datetime import datetime


class InsufficientBalanceError(Exception):
    """Raised when a debit/transfer is attempted with insufficient funds."""
    pass


class InvalidAmountError(Exception):
    """Raised when an amount <= 0 is passed to credit/debit/transfer."""
    pass


# mocking
class NotificationService:
    def send_notification(self, message: str):
        print(f"Notification: {message}")


class BankAccount:

    def __init__(self, owner: str, balance: float = 0.0, notifier=None):
        if balance < 0:
            raise InvalidAmountError("Initial balance cannot be negative.")

        self.owner = owner

        if notifier is not None:
            self.notifier = notifier
        else:
            self.notifier = NotificationService()

        self.balance = float(balance)

        self._transaction_history = []  # list of strings describing each transaction

        self._log(
            f"Account created for {owner} with balance {self.balance}"
        )

    # ---------- internal helper ----------
    def _log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._transaction_history.append(f"[{timestamp}] {message}")

    # ---------- 1. credit ----------
    def credit(self, amount: float):
        """Deposit money into the account."""
        if amount <= 0:
            raise InvalidAmountError(
                "Credit amount must be greater than zero."
            )

        self.balance += amount

        self._log(
            f"Credited {amount}. New balance: {self.balance}"
        )

        return self.balance

    # ---------- 2. debit ----------
    def debit(self, amount: float):
        """Withdraw money from the account."""
        if amount <= 0:
            raise InvalidAmountError(
                "Debit amount must be greater than zero."
            )

        if amount > self.balance:
            raise InsufficientBalanceError(
                f"Insufficient balance. Available: {self.balance}, "
                f"Requested: {amount}"
            )

        self.balance -= amount

        self._log(
            f"Debited {amount}. New balance: {self.balance}"
        )

        return self.balance

    # ---------- 3. UPI transfer ----------
    def upi_transfer(self, other_account: "BankAccount", amount: float):
        """Transfer money from this account to another BankAccount (UPI style)."""

        if not isinstance(other_account, BankAccount):
            raise TypeError(
                "other_account must be a BankAccount instance."
            )

        if amount <= 0:
            raise InvalidAmountError(
                "Transfer amount must be greater than zero."
            )

        if amount > self.balance:
            raise InsufficientBalanceError(
                f"Insufficient balance for UPI transfer. "
                f"Available: {self.balance}"
            )

        # Debit from sender, credit to receiver
        self.balance -= amount
        other_account.balance += amount

        self._log(
            f"UPI transferred {amount} to {other_account.owner}. "
            f"New balance: {self.balance}"
        )

        other_account._log(
            f"UPI received {amount} from {self.owner}. "
            f"New balance: {other_account.balance}"
        )

        self.notifier.send_notification(
            f"{amount} transferred from {self.owner} to {other_account.owner}"
        )

        return self.balance

    # ---------- 4. get balance ----------
    def get_balance(self):
        """Return the current account balance."""
        return self.balance

    # ---------- 5. apply interest ----------
    def apply_interest(self, rate_percent: float):
        """Apply a simple interest rate (in %) on the current balance."""

        if rate_percent < 0:
            raise InvalidAmountError(
                "Interest rate cannot be negative."
            )

        interest = self.balance * (rate_percent / 100)
        self.balance += interest

        self._log(
            f"Applied {rate_percent}% interest ({interest:.2f}). "
            f"New balance: {self.balance}"
        )

        return self.balance

    # ---------- 6. get transaction history ----------
    def get_transaction_history(self):
        """Return the list of all transactions performed on this account."""
        return self._transaction_history

    def __repr__(self):
        return (
            f"BankAccount(owner='{self.owner}', "
            f"balance={self.balance})"
        )