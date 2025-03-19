import allure
from faker import Faker
from api.BoardApi import BoardApi

fake = Faker()

def test_create_user(api_client: BoardApi):
    accountType = "INDIVIDUAL"
    email = fake.email()
    name = fake.name()
    password = fake.password(length=20, special_chars=False, digits=True, upper_case=True, lower_case=True)

    user_list_before = api_client.get_users()
    api_client.create_user(accountType, email, name, password)
    user_list_after = api_client.get_users()

    with allure.step("Проверить, что список общего количества юзеров увеличился на одного после добавления нового юзера"):
        assert len(user_list_after) - len(user_list_before) == 1

    last_user = user_list_after[-1]

    with allure.step("Проверить, что имя и email последнего созданного юзера совпадают с ожидаемыми"):
        assert last_user["name"] == name, f"Имя не совпадает! Ожидалось: {name}, Получено: {last_user['name']}"
        assert last_user["email"] == email, f"Email не совпадает! Ожидалось: {email}, Получено: {last_user['email']}"

def test_change_username(api_client: BoardApi):
    accountType = "INDIVIDUAL"
    email = fake.email()
    name = fake.name()
    password = fake.password(length=20, special_chars=False, digits=True, upper_case=True, lower_case=True)

    api_client.create_user(accountType, email, name, password)

    user_list = api_client.get_users()

    assert user_list, "Список пользователей пуст!"

    last_user = user_list[-1]
    user_id = last_user["id"]

    new_name = fake.name()
    pronouns = fake.prefix()

    api_client.edit_name_pronouns(user_id, new_name, pronouns)

    updated_user = api_client.get_user_by_ID(user_id)
    print(f"Обновленные данные последнего пользователя: {updated_user}")

    with allure.step("Проверить, что имя и обращение последнего созданного юзера изменились"):
        assert updated_user["name"] == new_name, f"Имя не изменилось! Ожидалось: {new_name}, Получено: {updated_user['name']}"
        assert updated_user["pronouns"] == pronouns, f"Обращение не изменилось! Ожидалось: {pronouns}, Получено: {updated_user['pronouns']}"