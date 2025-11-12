from models.client import Client
from models.account import Account
from models.transaction import Transaction

class Bank:
    """Фасад управления клиентами, счетами и транзакциями."""

    def __init__(self, name):
        self.name = name
        print(f"🏦 Банк «{self.name}» инициализирован.")

    # === Работа с клиентами ===
    def add_client(self, name: str, email: str) -> Client:
        client = Client(name=name, email=email).save()
        print(f"✅ Клиент создан: {client.name} ({client.email})")
        return client

    def list_clients(self):
        clients = Client.list_all()
        if not clients:
            print("📭 Клиентов пока нет.")
        else:
            print("\n=== СПИСОК КЛИЕНТОВ ===")
            for c in clients:
                print(f"{c.id}. {c.name} | {c.email}")

    # === Работа со счетами ===
    def open_account(self, client_id: int, currency: str, balance: float = 0.0):
        acc = Account(client_id=client_id, balance=balance, currency=currency).save()
        print(f"💳 Открыт счёт ID={acc.id} для клиента {client_id} ({currency})")
        return acc

    def list_accounts(self, client_id: int):
        accs = Account.list_by_client(client_id)
        if not accs:
            print("📭 У клиента нет счетов.")
            return
        print(f"\n=== СЧЕТА КЛИЕНТА #{client_id} ===")
        for a in accs:
            print(f"ID:{a.id} | Баланс:{a.balance:.2f} {a.currency} | Статус:{a.status}")

    # === Транзакции ===
    def deposit(self, acc_id: int, amount: float):
        tr = Transaction.deposit(acc_id, amount)
        print(f"💰 Депозит {amount} на счёт {acc_id} (ID транзакции {tr.id})")

    def withdraw(self, acc_id: int, amount: float):
        tr = Transaction.withdraw(acc_id, amount)
        print(f"💸 Снятие {amount} со счёта {acc_id} (ID транзакции {tr.id})")

    def transfer(self, from_id: int, to_id: int, amount: float):
        tr = Transaction.transfer(from_id, to_id, amount)
        print(f"🔁 Перевод {amount} от счёта {from_id} к счёту {to_id} (ID транзакции {tr.id})")

    def show_transactions(self):
        trs = Transaction.list_all()
        if not trs:
            print("📭 Транзакций пока нет.")
            return
        print("\n=== ИСТОРИЯ ТРАНЗАКЦИЙ ===")
        for t in trs:
            print(f"#{t[0]} | {t[4]} | от:{t[1]} → к:{t[2]} | сумма:{t[3]} | время:{t[5]}")
