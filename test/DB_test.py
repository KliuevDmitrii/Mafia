import allure
import pytest
from faker import Faker
from db.MafiaTable import MafiaTable


fake = Faker()

@allure.title("Тестирование добавления нового пользователя")
def test_add_user(db_session):
    mafia = MafiaTable(db_session)

    # Подготовка данных
    name = fake.name()
    email = fake.email()
    raw_password = fake.password(length=10)
    hashed_password = MafiaTable.hash_password(raw_password)
    role = "USER"
    account_type = "INDIVIDUAL"
    call_access = "NEED_CARD"
    is_email_confirm = False

    # Кол-во до
    users_before = mafia.get_all_users()
    count_before = len(users_before)

    with allure.step(f"Добавление пользователя с email: {email}"):
        mafia.add_user(
            name=name,
            email=email,
            password=hashed_password,
            role=role,
            account_type=account_type,
            call_create_access=call_access,
            is_email_confirm=is_email_confirm
        )

    # Кол-во после
    users_after = mafia.get_all_users()
    count_after = len(users_after)

    with allure.step("Проверка, что количество пользователей увеличилось на 1"):
        assert count_after - count_before == 1, (
            f"Ожидалось увеличение на 1. Было: {count_before}, стало: {count_after}"
        )

    with allure.step("Проверка, что пользователь действительно добавлен"):
        user = mafia.get_user_by_email(email)
        assert user is not None and user != {}, "Пользователь не найден в базе"
        assert user["email"] == email
        assert user["name"] == name
        assert user["role"] == role

@allure.title("Тест изменения имени и местоимений пользователя")
def test_update_user_fields(db_session):
    mafia = MafiaTable(db_session)

    # Подготовка исходных данных
    name = fake.name()
    email = fake.email()
    raw_password = fake.password(length=10)
    hashed_password = MafiaTable.hash_password(raw_password)
    role = "USER"
    account_type = "INDIVIDUAL"
    call_access = "NEED_CARD"
    is_email_confirm = False

    with allure.step("Создание нового пользователя"):
        mafia.add_user(
            name=name,
            email=email,
            password=hashed_password,
            role=role,
            account_type=account_type,
            call_create_access=call_access,
            is_email_confirm=is_email_confirm
        )

    user = mafia.get_user_by_email(email)
    assert user, f"Пользователь {email} не найден после добавления"
    user_id = user["id"]

    # Новые значения
    new_name = fake.name()
    new_pronouns = fake.prefix()

    with allure.step("Обновление имени и местоимений пользователя"):
        mafia.update_user(user_id=user_id, name=new_name, pronouns=new_pronouns)

    updated_user = mafia.get_user_by_email(email)

    with allure.step("Проверка обновлённых данных"):
        assert updated_user["name"] == new_name, f"Имя не обновлено: {updated_user['name']} ≠ {new_name}"
        assert updated_user["pronouns"] == new_pronouns, f"Местоимения не обновлены: {updated_user['pronouns']} ≠ {new_pronouns}"

@allure.title("Создание и удаление пользователя в БД")
def test_create_and_delete_user(db_session):
    mafia = MafiaTable(db_session)

    # Подготовка данных
    name = fake.name()
    email = fake.email()
    raw_password = fake.password(length=10)
    hashed_password = MafiaTable.hash_password(raw_password)
    role = "USER"
    account_type = "INDIVIDUAL"
    call_access = "NEED_CARD"
    is_email_confirm = False

    with allure.step("Создание нового пользователя"):
        mafia.add_user(
            name=name,
            email=email,
            password=hashed_password,
            role=role,
            account_type=account_type,
            call_create_access=call_access,
            is_email_confirm=is_email_confirm
        )

    with allure.step("Проверка, что пользователь создан"):
        user = mafia.get_user_by_email(email)
        assert user, f"Пользователь с email {email} не найден после создания"
        assert user["email"] == email
        user_id = user["id"]

    with allure.step("Удаление пользователя"):
        mafia.delete_user_by_id(user_id)

    with allure.step("Проверка, что пользователь удалён"):
        deleted_user = mafia.get_user_by_email(email)
        assert not deleted_user, "Пользователь всё ещё существует после удаления"

