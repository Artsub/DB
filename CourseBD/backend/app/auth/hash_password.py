from passlib.context import CryptContext

# Инициализация CryptContext с правильными параметрами
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Класс для работы с паролями
class HashPassword:
    @staticmethod
    def bcrypt(password: str) -> str:
        """Хеширует пароль с использованием bcrypt"""
        return password

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        """Проверяет соответствие хеша и пароля"""
        return plain_password == hashed_password
