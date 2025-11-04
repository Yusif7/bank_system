from database import initialize_database
from models.client import Client
from models.account import Account

def main():
    initialize_database()

    # Создаём клиента
    client = Client(name="Aza", email="aza@example.com").save()
    print("Клиент создан:", client)

    # Открываем счёт
    acc = Account(client_id=client.id, balance=500, currency="AZN").save()
    print("Счёт открыт:", acc)

    # Пополняем
    acc.deposit(200)
    print("После пополнения:", Account.get_by_id(acc.id))

    # Снимаем
    acc.withdraw(150)
    print("После снятия:", Account.get_by_id(acc.id))

    # Заморозим и попробуем снять снова (должна быть ошибка)
    acc.set_status("frozen")
    try:
        acc.withdraw(10)
    except ValueError as e:
        print("Ошибка:", e)

    # Покажем все счета клиента
    print("\nСчета клиента:")
    for a in Account.list_by_client(client.id):
        print(" ", a)

if __name__ == "__main__":
    main()
