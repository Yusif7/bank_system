import sqlite3
from contextlib import contextmanager

DB_NAME = "bank.db"

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    # включаем внешние ключи в SQLite.
    # Эта строка включает их поддержку, чтобы SQLite соблюдал связи между таблицами и не позволял удалять/вставлять несовместимые данные.
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        # Превращает функцию в генератор, функция работает до yield и оставливается
        # yield нужен когда нельзя (или не хочется) вернуть всё сразу.
        yield conn # ← тут “пауза”: даём пользователю поработать
        conn.commit() # ← возобновление: сохраняем изменения
    finally:
        conn.close()

def initialize_database():
    with get_connection() as conn:
        cur = conn.cursor()

        # Клиенты
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            email       TEXT UNIQUE NOT NULL,
            created_at  TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Счета
        # ON DELETE CASCADE у счетов — если удалим клиента, его счета удалятся.
        cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id   INTEGER NOT NULL,
            balance     REAL NOT NULL CHECK(balance >= 0),
            currency    TEXT NOT NULL CHECK(currency IN ('AZN','USD','EUR')),
            status      TEXT NOT NULL CHECK(status IN ('active','frozen','closed')),
            created_at  TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE 
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_accounts_client ON accounts(client_id);")

        # Транзакции
        cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            from_account  INTEGER,
            to_account    INTEGER,
            amount        REAL NOT NULL CHECK(amount > 0),
            type          TEXT NOT NULL CHECK(type IN ('deposit','withdraw','transfer')),
            timestamp     TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (from_account) REFERENCES accounts(id) ON DELETE SET NULL,
            FOREIGN KEY (to_account)   REFERENCES accounts(id) ON DELETE SET NULL
        );
        """)
