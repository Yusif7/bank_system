from database import initialize_database
from models.client import Client
from models.account import Account
from models.transaction import Transaction

def main():
    initialize_database()

    # создаём клиентов
    c1 = Client(name="Murad", email="Murad@example.com").save()
    c2 = Client(name="Vasif", email="vasif@example.com").save()
    client_list = [c1,c2]
    for client in client_list:
        print("Клиент создан:", client)

    # открываем счета
    a1 = Account(client_id=c1.id, balance=500, currency="AZN").save()
    a2 = Account(client_id=c2.id, balance=1000, currency="AZN").save()

    # депозит
    Transaction.deposit(a1.id, 200)
    # снятие
    Transaction.withdraw(a2.id, 150)
    # перевод
    Transaction.transfer(a1.id, a2.id, 100)

    print("\n=== Список всех транзакций ===")
    for tr in Transaction.list_all():
        print(tr)

if __name__ == "__main__":
    main()
