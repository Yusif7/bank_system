from database import initialize_database
from models.client import Client

def main():
    initialize_database()

    # 1) Создаём клиента
    c = Client(name="Yusif", email="yusif@example.com").save()
    print("Создан:", c)

    # 2) Загружаем по id
    same = Client.get_by_id(c.id)
    print("Загружен:", same)

    # 3) Обновляем
    same.update(name="Yusif Osmanov")
    print("Обновлён:", Client.get_by_id(same.id))

    # 4) Список всех
    print("Все клиенты:")
    for cli in Client.list_all():
        print(" -", cli)

    # 5) Удаляем
    same.delete()
    print("После удаления get_by_id ->", Client.get_by_id(c.id))

if __name__ == "__main__":
    main()