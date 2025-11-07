from dataclasses import dataclass
from database import get_connection
from models.account import Account

@dataclass
class Transaction:
    from_account: int | None
    to_account: int | None
    amount: float
    type: str
    id: int | None = None

    def save(self):
        if self.amount <= 0:
            raise ValueError("Сумма транзакции должна быть положительной.")
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO transactions (from_account, to_account, amount, type)
                VALUES (?, ?, ?, ?)
            """, (self.from_account, self.to_account, self.amount, self.type))
            self.id = cur.lastrowid
        return self

    # === Выполнение депозита ===
    @staticmethod
    def deposit(to_account_id: int, amount: float):
        acc = Account.get_by_id(to_account_id)
        if not acc:
            raise ValueError("Счёт не найден.")
        acc.deposit(amount)
        tr = Transaction(from_account=None, to_account=to_account_id, amount=amount, type="deposit").save()
        return tr

    # === Снятие денег ===
    @staticmethod
    def withdraw(from_account_id: int, amount: float):
        acc = Account.get_by_id(from_account_id)
        if not acc:
            raise ValueError("Счёт не найден.")
        acc.withdraw(amount)
        tr = Transaction(from_account=from_account_id, to_account=None, amount=amount, type="withdraw").save()
        return tr

    # === Перевод между счетами ===
    @staticmethod
    def transfer(from_account_id: int, to_account_id: int, amount: float):
        from_acc = Account.get_by_id(from_account_id)
        to_acc = Account.get_by_id(to_account_id)
        if not from_acc or not to_acc:
            raise ValueError("Один из счетов не найден.")
        if from_acc.currency != to_acc.currency:
            raise ValueError("Нельзя переводить между счетами с разной валютой.")
        from_acc.withdraw(amount)
        to_acc.deposit(amount)
        tr = Transaction(from_account=from_account_id, to_account=to_account_id, amount=amount, type="transfer").save()
        return tr

    @staticmethod
    def list_all():
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, from_account, to_account, amount, type, timestamp
                FROM transactions ORDER BY id DESC
            """)
            rows = cur.fetchall()
        return rows
