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

def test_change_username(api_client: BoardApi):
    accountType = "INDIVIDUAL"
    email = fake.email()
    name = fake.name()
    password = fake.password(length=20, special_chars=False, digits=True, upper_case=True, lower_case=True)

    new_user = api_client.create_user(accountType, email, name, password)

    user_id = new_user.get('id')

    new_name = fake.name()
    pronouns = fake.prefix()

    api_client.edit_name_pronouns(user_id, new_name, pronouns)

    updated_user = api_client.get_user_by_ID(user_id)
    print(f"Обновленные данные пользователя: {updated_user}")

    with allure.step("Проверить, что у юзера сменилось имя и обращение"):
        assert updated_user["name"] == new_name, "Имя не изменилось!"
        assert updated_user["pronouns"] == pronouns, "Обращение не изменилось!"