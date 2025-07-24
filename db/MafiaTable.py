from sqlalchemy.orm import Session
import bcrypt
from sqlalchemy import text
import allure


class MafiaTable:
    """
    Класс для выполнения запросов к таблицам проекта Ludio/Mafia.
    Использует переданную SQLAlchemy-сессию.
    """

    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    @allure.step("Хеширование пароля")
    def hash_password(password: str, salt_rounds: int = 10) -> str:
        salt = bcrypt.gensalt(rounds=salt_rounds)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    # Методы для работы с пользователями в таблице "users"

    @allure.step("Добавить нового пользователя")
    def add_user(self, name: str, email: str, password: str, role: str = "USER",
                 account_type: str = "INDIVIDUAL", call_create_access: str = "NEED_CARD",
                 is_email_confirm: bool = False) -> None:
        """
        Добавляет нового пользователя с полным набором полей.
        Пароль будет захеширован.
        """
        hashed_password = self.hash_password(password)

        query = text("""
            INSERT INTO public."users"
            ("name", email, "password", "role", "accountType", "callCreateAccess", "isEmailConfirm")
            VALUES (:name, :email, :password, :role, :account_type, :call_create_access, :is_email_confirm)
        """)

        self.session.execute(query, {
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": role,
            "account_type": account_type,
            "call_create_access": call_create_access,
            "is_email_confirm": is_email_confirm
        })

        self.session.commit()

    @allure.step("Получить пользователя по email")
    def get_user_by_email(self, email: str) -> dict:
        """
        Получить пользователя по email
        """
        query = text("""
            SELECT id, email, name, role, created_at, pronouns
            FROM public."users"
            WHERE email = :email
            LIMIT 1
        """)
        result = self.session.execute(query, {"email": email}).mappings().first()
        return dict(result) if result else {}
    
    @allure.step("Получить пользователя по ID")
    def get_user_by_id(self, id: str) -> dict:
        """
        Получить пользователя по ID
        """
        query = text("""
            SELECT id, email, name, role, created_at
            FROM public."users"
            WHERE id = :id
            LIMIT 1
        """)
        result = self.session.execute(query, {"id": id}).mappings().first()
        return dict(result) if result else {}
    
    @allure.step("Получить пользователя по имени")
    def get_user_by_name(self, name: str) -> dict:
        """
        Получить пользователя по имени
        """
        query = text("""
            SELECT id, email, name, role, created_at
            FROM public."users"
            WHERE name = :name
            LIMIT 1
        """)
        result = self.session.execute(query, {"name": name}).mappings().first()
        return dict(result) if result else {}
    
    @allure.step("Изменить данные пользователя")
    def update_user(self, user_id: str, name: str = None, pronouns: str = None):
        """
        Обновляет указанные поля пользователя по ID.
        Обновляются только те поля, которые не равны None.
        """
        fields_to_update = {}
        if name is not None:
            fields_to_update["name"] = name
        if pronouns is not None:
            fields_to_update["pronouns"] = pronouns

        if not fields_to_update:
            raise ValueError("Не переданы данные для обновления")

        # Динамически формируем часть SET name = :name, pronouns = :pronouns
        set_clause = ", ".join([f'{key} = :{key}' for key in fields_to_update.keys()])
        fields_to_update["user_id"] = user_id

        query = text(f"""
            UPDATE public."users"
            SET {set_clause}
            WHERE id = :user_id
        """)

        self.session.execute(query, fields_to_update)
        self.session.commit()

    @allure.step("Удалить пользователя по ID")
    def delete_user_by_id(self, user_id: str) -> None:
        """
        Удаляет пользователя по ID.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"Пользователь с ID {user_id} не найден")
        
        query = text("""
            DELETE FROM public."users"
            WHERE id = :user_id
        """)
        self.session.execute(query, {"user_id": user_id})
        self.session.commit()
    
    @allure.step("Получить всех пользователей")
    def get_all_users(self) -> list:
        """
        Получить всех пользователей
        """
        query = text("""
            SELECT *
            FROM public."users"
        """)
        results = self.session.execute(query).mappings().all()
        return [dict(result) for result in results]
    
    # Методы для работы с токенами в таблице "confirmTokensers"
