from dataclasses import dataclass
from database import get_connection

@dataclass
class Account:
    client_id: int
    balance: float
    currency: str
    status: str = "active"
    id: int | None = None

    # === Создание счёта ===
    def save(self):
        if self.currency not in ("AZN", "USD", "EUR"):
            raise ValueError("Недопустимая валюта")
        if self.balance < 0:
            raise ValueError("Баланс не может быть отрицательным.")
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO accounts (client_id, balance, currency, status)
                VALUES (?, ?, ?, ?)
            """, (self.client_id, self.balance, self.currency, self.status))
            self.id = cur.lastrowid
        return self

    # === Пополнение счёта ===
    def deposit(self, amount: float):
        if self.status != "active":
            raise ValueError("Счёт не активен.")
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной.")
        self.balance += amount
        with get_connection() as conn:
            conn.execute("UPDATE accounts SET balance = ? WHERE id = ?", (self.balance, self.id))
        return self

    # === Снятие денег ===
    def withdraw(self, amount: float):
        if self.status != "active":
            raise ValueError("Счёт не активен.")
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной.")
        if amount > self.balance:
            raise ValueError("Недостаточно средств.")
        self.balance -= amount
        with get_connection() as conn:
            conn.execute("UPDATE accounts SET balance = ? WHERE id = ?", (self.balance, self.id))
        return self

    # === Заморозка/разморозка/закрытие ===
    def set_status(self, new_status: str):
        if new_status not in ("active", "frozen", "closed"):
            raise ValueError("Недопустимый статус.")
        self.status = new_status
        with get_connection() as conn:
            conn.execute("UPDATE accounts SET status = ? WHERE id = ?", (new_status, self.id))
        return self

    # === Загрузка ===
    @staticmethod
    def get_by_id(account_id: int) -> "Account | None":
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, client_id, balance, currency, status FROM accounts WHERE id = ?", (account_id,))
            row = cur.fetchone()
        if not row:
            return None
        return Account(id=row[0], client_id=row[1], balance=row[2], currency=row[3], status=row[4])

    @staticmethod
    def list_by_client(client_id: int) -> list["Account"]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, client_id, balance, currency, status
                FROM accounts WHERE client_id = ?
            """, (client_id,))
            rows = cur.fetchall()
        return [Account(id=r[0], client_id=r[1], balance=r[2], currency=r[3], status=r[4]) for r in rows]
