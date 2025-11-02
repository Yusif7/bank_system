from dataclasses import dataclass
from database import get_connection

@dataclass
class Client:
    name: str
    email: str
    id: int | None = None

    # Создать клиента в БД
    def save(self):
        if not self.name or not self.email:
            raise ValueError("Имя и email обязательны.")
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO clients(name, email) VALUES(?, ?)",
                (self.name, self.email)
            )
            self.id = cur.lastrowid
        return self

    # Обновить имя/email клиента
    def update(self, *, name: str | None = None, email: str | None = None):
        if self.id is None:
            raise ValueError("Нельзя обновлять несохранённого клиента (id=None).")
        fields, params = [], []
        if name is not None:
            fields.append("name = ?")
            params.append(name)
        if email is not None:
            fields.append("email = ?")
            params.append(email)
        if not fields:
            return self
        params.append(self.id)
        with get_connection() as conn:
            conn.execute(f"UPDATE clients SET {', '.join(fields)} WHERE id = ?", params)
        if name is not None: self.name = name
        if email is not None: self.email = email
        return self

    # Удалить клиента
    def delete(self):
        if self.id is None:
            return
        with get_connection() as conn:
            conn.execute("DELETE FROM clients WHERE id = ?", (self.id,))
        self.id = None

    @staticmethod
    def get_by_id(client_id: int) -> "Client | None":
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name, email FROM clients WHERE id = ?", (client_id,))
            row = cur.fetchone()
        if not row:
            return None
        return Client(id=row[0], name=row[1], email=row[2])

    @staticmethod
    def list_all() -> list["Client"]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name, email FROM clients ORDER BY id;")
            rows = cur.fetchall()
        return [Client(id=r[0], name=r[1], email=r[2]) for r in rows]
