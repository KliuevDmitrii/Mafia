import allure
import pytest
from faker import Faker
from api.MafiaApi import MafiaApi
from testdata.DataProvider import DataProvider

fake = Faker()

@allure.title("Проверка создания пользователя с типом INDIVIDUAL")
def test_create_user_individual(api_client: MafiaApi):
    """
    Тест создания пользователя с типом аккаунта INDIVIDUAL.
    Проверяет:
    1. Увеличение количества пользователей после создания
    2. Корректность данных созданного пользователя
    """
    
    accountType = "INDIVIDUAL"
    email = fake.email()
    name = fake.name()
    password = fake.password(length=20, special_chars=False, digits=True, 
                           upper_case=True, lower_case=True)

    user_list_before = api_client.get_users()
    
    api_client.create_user(accountType, email, name, password)
    
    user_list_after = api_client.get_users()

    with allure.step("Проверить, что список общего количества юзеров увеличился на одного после добавления нового юзера"):
        assert len(user_list_after) - len(user_list_before) == 1, (
            f"Ожидалось увеличение на 1 пользователя. "
            f"Было: {len(user_list_before)}, стало: {len(user_list_after)}"
        )

    last_user = user_list_after[-1]

    with allure.step("Проверить, что имя и email последнего созданного юзера совпадают с ожидаемыми"):
        assert last_user["name"] == name, (
            f"Имя не совпадает! Ожидалось: {name}, Получено: {last_user['name']}"
        )
        assert last_user["email"] == email, (
            f"Email не совпадает! Ожидалось: {email}, Получено: {last_user['email']}"
        )

@allure.title("Тест создания пользователя с типом ORGANIZATION")
def test_create_user_organization(api_client: MafiaApi):
    """
    Тест проверяет корректное создание пользователя с типом ORGANIZATION.
    Проверяет:
    1. Увеличение общего количества пользователей после создания
    2. Соответствие данных созданного пользователя переданным значениям
    """
    
    accountType = "ORGANIZATION"
    email = f"{fake.user_name()}@hi2.in"
    name = fake.name()
    password = fake.password(length=20, special_chars=False, 
                           digits=True, upper_case=True, lower_case=True)

    user_list_before = api_client.get_users()
    
    api_client.create_user(accountType, email, name, password)
    
    user_list_after = api_client.get_users()

    with allure.step("Проверка увеличения количества пользователей"):
        assert len(user_list_after) - len(user_list_before) == 1, (
            f"Ожидалось увеличение на 1 пользователя. "
            f"Было: {len(user_list_before)}, стало: {len(user_list_after)}"
        )

    last_user = user_list_after[-1]

    with allure.step("Проверка данных созданного пользователя"):
        assert last_user["name"] == name, (
            f"Несоответствие имени. Ожидалось: {name}, получено: {last_user['name']}"
        )
        assert last_user["email"] == email, (
            f"Несоответствие email. Ожидалось: {email}, получено: {last_user['email']}"
        )
        assert last_user["accountType"] == accountType, (
            f"Несоответствие типа аккаунта. "
            f"Ожидалось: {accountType}, получено: {last_user['accountType']}"
        )

@allure.title("Тест изменения имени и обращения нового пользователя")
def test_change_username(api_client: MafiaApi):
    """
    Тест проверяет функциональность изменения имени и обращения пользователя.
    Проверяет:
    1. Создание тестового пользователя
    2. Корректность изменения имени
    3. Корректность изменения обращения
    """

    accountType = "INDIVIDUAL"
    email = fake.email()
    initial_name = fake.name()
    password = fake.password(length=20, special_chars=False, 
                          digits=True, upper_case=True, lower_case=True)

    with allure.step("Создание тестового пользователя"):
        api_client.create_user(accountType, email, initial_name, password)
    
    with allure.step("Получение списка пользователей"):
        user_list = api_client.get_users()
        assert user_list, "Список пользователей пуст! Не удалось создать тестового пользователя"
    
    last_user = user_list[-1]
    user_id = last_user["id"]
    allure.attach(str(user_id), name="User ID", attachment_type=allure.attachment_type.TEXT)

    new_name = fake.name()
    pronouns = fake.prefix()
    allure.attach(f"Новые данные:\nИмя: {new_name}\nОбращение: {pronouns}", 
                 name="New User Data", 
                 attachment_type=allure.attachment_type.TEXT)

    with allure.step("Изменение имени и обращения пользователя"):
        api_client.edit_name_pronouns(user_id, new_name, pronouns)
    
    with allure.step("Получение обновленных данных пользователя"):
        updated_user = api_client.get_user_by_ID(user_id)
        print(f"Обновленные данные пользователя: {updated_user}")
        allure.attach(str(updated_user), 
                     name="Updated User Data", 
                     attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверка изменений данных пользователя"):
        assert updated_user["name"] == new_name, (
            f"Имя не было изменено корректно. "
            f"Ожидалось: {new_name}, Фактическое: {updated_user['name']}"
        )
        
        assert updated_user["pronouns"] == pronouns, (
            f"Обращение не было изменено корректно. "
            f"Ожидалось: {pronouns}, Фактическое: {updated_user['pronouns']}"
        )

@allure.title("Тест изменения имени и обращения авторизованного пользователя")
def test_change_username_authorized_user(authorized_api_client):
    """
    Тест проверяет функциональность изменения имени и обращения 
    авторизованного пользователя INDIVIDUAL из test_data.json
    """

    user_email = DataProvider().get("INDIVIDUAL")["email"]

    with allure.step("Получение списка пользователей"):
        users = authorized_api_client.get_users()
        assert isinstance(users, list) and users, "Не удалось получить список пользователей"

    target_user = next((user for user in users if user.get("email") == user_email), None)
    assert target_user is not None, f"Пользователь с email {user_email} не найден"

    user_id = target_user["id"]
    allure.attach(str(user_id), name="User ID", attachment_type=allure.attachment_type.TEXT)

    new_name = fake.name()
    pronouns = fake.prefix()

    allure.attach(f"Новые данные:\nИмя: {new_name}\nОбращение: {pronouns}", 
                  name="New User Data", 
                  attachment_type=allure.attachment_type.TEXT)

    with allure.step("Изменение имени и обращения пользователя"):
        response = authorized_api_client.edit_name_pronouns(user_id, new_name, pronouns)
        assert not response.get("error"), f"Ошибка изменения имени/обращения: {response.get('error')}"

    with allure.step("Получение обновленных данных пользователя"):
        updated_user = authorized_api_client.get_user_by_ID(user_id)
        allure.attach(str(updated_user), 
                      name="Updated User Data", 
                      attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверка применённых изменений"):
        assert updated_user["name"] == new_name, (
            f"Имя не было изменено. Ожидалось: {new_name}, Фактически: {updated_user['name']}"
        )
        assert updated_user["pronouns"] == pronouns, (
            f"Обращение не было изменено. Ожидалось: {pronouns}, Фактически: {updated_user['pronouns']}"
        )

@allure.title("Проверка статус-кода 401 при авторизации с невалидным паролем")
def test_negative_login_user_invalid_password(api_client: MafiaApi, test_data: DataProvider):
    """
    Тест проверяет, что при попытке авторизации с невалидным паролем
    возвращается статус-код 401 (Unauthorized) с соответствующим сообщением об ошибке.
    """

    user_data = test_data.get("INDIVIDUAL")
    if not user_data:
        pytest.fail("Нет данных для INDIVIDUAL пользователя")

    email = user_data.get("email")
    valid_password = user_data.get("pass")
    invalid_password = valid_password + "не валидный"

    with allure.step(f"Попытка авторизации с email {email} и невалидным паролем"):
        response = api_client.auth_user(email, invalid_password)
        print(f"Response: {response}")

    with allure.step("Проверка статус-кода ответа"):
        status_code = response.get("statusCode") 
        assert status_code == 401, (
            f"Ожидался статус-код 401, но получен {status_code}. "
            f"Ответ сервера: {response}"
        )

    with allure.step("Проверка сообщения об ошибке"):
        error_message = response.get("message", "")
        assert "not valid" in error_message.lower(), (
            f"Ожидалось сообщение об ошибке авторизации, но получено: {error_message}"
        )

@allure.title("Проверка статус-кода 404 при авторизации с несуществующим логином")
def test_negative_login_invalid_username(api_client: MafiaApi, test_data: DataProvider):
    """
    Тест проверяет, что при попытке авторизации с несуществующим email
    возвращается статус-код 404 (Not Found) с соответствующим сообщением об ошибке.
    """
    
    user_data = test_data.get("INDIVIDUAL")
    if not user_data:
        pytest.fail("Нет данных для INDIVIDUAL пользователя")

    invalid_email = f"nonexistent_{fake.user_name()}@example.com"
    valid_password = user_data.get("pass")

    with allure.step(f"Попытка авторизации с несуществующим email {invalid_email}"):
        response = api_client.auth_user(invalid_email, valid_password)
        print(f"Response: {response}")

    with allure.step("Проверка статус-кода ответа"):
        status_code = response.get("statusCode") 
        assert status_code == 404, (
            f"Ожидался статус-код 404 (Not Found), но получен {status_code}. "
            f"Полный ответ сервера: {response}"
        )

    with allure.step("Проверка сообщения об ошибке"):
        error_message = response.get("message", "").lower()
        expected_phrases = ["not found", "user not exist", "не найден"]
        assert any(phrase in error_message for phrase in expected_phrases), (
            f"Ожидалось сообщение о ненайденном пользователе, но получено: {error_message}"
        )

@allure.title("Проверка создания пользователя с существующим email (ожидается 409 Conflict)")
def test_create_user_with_existing_email(api_client: MafiaApi, test_data: DataProvider):
    """
   Проверяет корректность обработки попытки регистрации пользователя с уже существующим email.
    
    Ожидаемое поведение API:
    1. Должен вернуть HTTP статус 409 Conflict
    2. В теле ответа должно быть:
       - Стандартное описание ошибки
       - Четкое указание на конфликт email
       - Корректная структура ошибки согласно API спецификации
   """
    
    user_data = test_data.get("INDIVIDUAL")
    if not user_data:
        pytest.fail("Нет данных для INDIVIDUAL пользователя в тестовых данных")

    accountType = "INDIVIDUAL"
    existing_email = user_data.get("email")
    name = fake.name()
    password = fake.password(length=20, special_chars=False, 
                           digits=True, upper_case=True, lower_case=True)

    with allure.step(f"Попытка регистрации с email {existing_email}"):
        response = api_client.create_user(accountType, existing_email, name, password)
        
        print(f"Response: {response}")
        allure.attach(str(response), name="API Response", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверка структуры ответа"):
        assert isinstance(response, dict), "Ответ должен быть словарем"
        assert "error" in response, "Ответ должен содержать поле 'error'"

    with allure.step("Проверка кода ошибки 409"):
        error_message = response["error"]
        assert "409" in error_message, (
            f"Ожидалась ошибка 409 Conflict, но получено: {error_message}"
        )

    with allure.step("Дополнительная проверка через GET запрос"):
        try:
            user_list = api_client.get_users()
            emails = [user["email"] for user in user_list]
            assert existing_email in emails, (
                f"Email {existing_email} не найден в списке пользователей после попытки повторной регистрации"
            )
        except Exception as e:
            pytest.fail(f"Ошибка при проверке списка пользователей: {str(e)}")

@allure.title("Проверка создания пользователя с невалидным паролем")
def test_negative_create_user_invalid_password(api_client: MafiaApi):
    """
    Тест проверяет обработку попытки регистрации с невалидным паролем.
    
    Ожидаемое поведение:
    1. API должен вернуть ошибку (400 Bad Request или 422 Unprocessable Entity)
    2. Сообщение об ошибке должно указывать на проблему с паролем
    3. Пользователь не должен быть создан в системе
    """

    accountType = "INDIVIDUAL"
    email = fake.email()
    name = fake.name()
    invalid_password = "123"

    user_list_before = api_client.get_users()
    
    response = api_client.create_user(accountType, email, name, invalid_password)
    allure.attach(str(response), name="Response", attachment_type=allure.attachment_type.JSON)

    user_list_after = api_client.get_users()

    with allure.step("Проверка что пользователь не был добавлен"):
        assert len(user_list_after) == len(user_list_before), (
            f"Количество пользователей не должно измениться. Было: {len(user_list_before)}, стало: {len(user_list_after)}"
        )
        
    emails_after = [user["email"] for user in user_list_after]

    with allure.step("Проверка что email не появился в системе"):
        assert email not in emails_after, (
            f"Пользователь с email {email} был создан, хотя пароль невалидный"
        )

@allure.title("Тест: сброс пароля возвращает статус 201 и поле ok=True")
def test_reset_password_status_201(authorized_api_client):
    """
    Проверка, что при сбросе пароля:
    - статус ответа = 201
    - тело ответа содержит {"ok": true}
    """
    email = DataProvider().get("INDIVIDUAL")["email"]

    with allure.step(f"Отправка запроса на сброс пароля для {email}"):
        status_code, response_json = authorized_api_client.reset_password(email)

        allure.attach(str(status_code), name="HTTP Status Code", attachment_type=allure.attachment_type.TEXT)
        allure.attach(str(response_json), name="Response JSON", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверка, что статус ответа — 201"):
        assert status_code == 201, f"Ожидался статус 201, но получен {status_code}"

    with allure.step("Проверка, что тело ответа содержит {'ok': true}"):
        assert response_json.get("ok") is True, "Ожидалось поле 'ok: true' в теле ответа"

@allure.title("Получение тарифов Stripe возвращает статус 200 и все ожидаемые поля")
def test_get_stripe_tariffs_status_and_fields(authorized_api_client):
    """
    Проверка, что при получении тарифов Stripe:
    - статус ответа = 200
    - тело ответа содержит все ожидаемые поля
    """
    with allure.step("Отправка запроса на получение тарифов Stripe"):
        data = authorized_api_client.get_stripe_tariffs()

        allure.attach(str(data), name="Stripe Tariffs Response", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверка, что ответ содержит все ключи"):
        expected_keys = [
            "everyDayStripePriceId",
            "monthStripePriceId",
            "quarterStripePriceId",
            "annualStripePriceId",
            "everyDayStripePrice",
            "monthStripePrice",
            "quarterStripePrice",
            "annualStripePrice",
            "dayPassStripePrice",
            "guestPassStripePrice"
        ]

        missing_keys = [key for key in expected_keys if key not in data]
        assert not missing_keys, f"В ответе отсутствуют ключи: {missing_keys}"
