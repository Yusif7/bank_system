from database import initialize_database
from models.bank import Bank

def main():
    initialize_database()
    bank = Bank("PythonBank")

    # 1. Создаём клиентов
    c1 = bank.add_client("Yusif", "yusif22@example.com")
    c2 = bank.add_client("Aza", "aza22@example.com")

    # 2. Открываем счета
    a1 = bank.open_account(c1.id, "AZN", 1000)
    a2 = bank.open_account(c2.id, "AZN", 500)

    # 3. Операции
    bank.deposit(a1.id, 250)
    bank.withdraw(a2.id, 100)
    bank.transfer(a1.id, a2.id, 200)

    # 4. Просмотр данных
    bank.list_clients()
    bank.list_accounts(c1.id)
    bank.list_accounts(c2.id)
    bank.show_transactions()

if __name__ == "__main__":
    main()
