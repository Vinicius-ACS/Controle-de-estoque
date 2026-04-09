from app.database import get_connection
from app.models import User


class UserRepository:
    def create(self, user: User) -> None:
        conn = get_connection()
        conn.execute(
            """
            INSERT INTO users (name, user_id, email, password)
            VALUES (?, ?, ?, ?)
            """,
            (user.name, user.user_id, user.email, user.password),
        )
        conn.commit()
        conn.close()

    def get_by_user_id(self, user_id: str) -> User | None:
        conn = get_connection()
        row = conn.execute(
            """
            SELECT id, name, user_id, email, password
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()
        conn.close()

        if row is None:
            return None

        return User(
            id=row["id"],
            name=row["name"],
            user_id=row["user_id"],
            email=row["email"],
            password=row["password"],
        )

    def get_by_email(self, email: str) -> User | None:
        conn = get_connection()
        row = conn.execute(
            """
            SELECT id, name, user_id, email, password
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()
        conn.close()

        if row is None:
            return None

        return User(
            id=row["id"],
            name=row["name"],
            user_id=row["user_id"],
            email=row["email"],
            password=row["password"],
        )

    def authenticate(self, user_id: str, password: str) -> User | None:
        conn = get_connection()
        row = conn.execute(
            """
            SELECT id, name, user_id, email, password
            FROM users
            WHERE user_id = ? AND password = ?
            """,
            (user_id, password),
        ).fetchone()
        conn.close()

        if row is None:
            return None

        return User(
            id=row["id"],
            name=row["name"],
            user_id=row["user_id"],
            email=row["email"],
            password=row["password"],
        )