import hashlib
from database import get_connection

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.role = role
        self.password = self.hash(password)

    def hash(self, text):
        return hashlib.sha256(text.encode()).hexdigest()

    def save(self):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (self.username, self.password, self.role)
            )
        print(f"👤 Пользователь '{self.username}' ({self.role}) создан.")

    @staticmethod
    def login(username, password):
        hash_ = hashlib.sha256(password.encode()).hexdigest()

        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT username, password, role FROM users WHERE username = ?",
                (username,)
            )
            row = cur.fetchone()

        if not row:
            print("❌ Пользователь не найден.")
            return None

        stored_hash = row[1]
        role = row[2]

        if hash_ != stored_hash:
            print("❌ Неверный пароль.")
            return None

        # Создание объекта правильного класса
        if role == "admin":
            return Admin(username, password)
        elif role == "manager":
            return Manager(username, password)
        else:
            return Cashier(username, password)

    def can(self, action):
        return action in self.get_permissions()


