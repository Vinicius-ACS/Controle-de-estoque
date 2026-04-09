from app.models import User
from app.userRepository import UserRepository
from app.validators import validate_user_data, validate_login_data


class UserService:
    def __init__(self) -> None:
        self.user_repo = UserRepository()

    def register_user(self, name: str, user_id: str, email: str, password: str) -> list[str]:
        errors = validate_user_data(name, user_id, email, password)
        if errors:
            return errors

        existing_user_id = self.user_repo.get_by_user_id(user_id.strip())
        if existing_user_id is not None:
            return ["Esse ID de usuário já está cadastrado."]

        existing_email = self.user_repo.get_by_email(email.strip())
        if existing_email is not None:
            return ["Esse e-mail já está cadastrado."]

        user = User(
            id=None,
            name=name.strip(),
            user_id=user_id.strip(),
            email=email.strip(),
            password=password.strip(),
        )
        self.user_repo.create(user)
        return []

    def login_user(self, user_id: str, password: str) -> tuple[list[str], User | None]:
        errors = validate_login_data(user_id, password)
        if errors:
            return errors, None

        user = self.user_repo.authenticate(user_id.strip(), password.strip())
        if user is None:
            return ["ID de usuário ou senha inválidos."], None

        return [], user