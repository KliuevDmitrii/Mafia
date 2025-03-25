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
    
    # Подготовка тестовых данных
    accountType = "INDIVIDUAL"  # Тип создаваемого аккаунта
    email = fake.email()  # Генерация случайного email
    name = fake.name()  # Генерация случайного имени
    # Генерация сложного пароля (20 символов: цифры, буквы в верхнем/нижнем регистре)
    password = fake.password(length=20, special_chars=False, digits=True, 
                           upper_case=True, lower_case=True)

    # Получаем список пользователей ДО создания нового
    user_list_before = api_client.get_users()
    
    # Создаем нового пользователя
    api_client.create_user(accountType, email, name, password)
    
    # Получаем список пользователей ПОСЛЕ создания
    user_list_after = api_client.get_users()

    # Проверка 1: Количество пользователей должно увеличиться на 1
    with allure.step("Проверить, что список общего количества юзеров увеличился на одного после добавления нового юзера"):
        assert len(user_list_after) - len(user_list_before) == 1, (
            f"Ожидалось увеличение на 1 пользователя. "
            f"Было: {len(user_list_before)}, стало: {len(user_list_after)}"
        )

    # Получаем данные последнего созданного пользователя
    last_user = user_list_after[-1]

    # Проверка 2: Данные созданного пользователя должны соответствовать переданным
    with allure.step("Проверить, что имя и email последнего созданного юзера совпадают с ожидаемыми"):
        # Проверка имени
        assert last_user["name"] == name, (
            f"Имя не совпадает! Ожидалось: {name}, Получено: {last_user['name']}"
        )
        # Проверка email
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
    
    # 1. Подготовка тестовых данных
    accountType = "ORGANIZATION"  # Тип создаваемого аккаунта
    email = f"{fake.user_name()}@hi2.in"  # Генерация email в специальном домене
    name = fake.name()  # Генерация случайного имени
    # Генерация сложного пароля (20 символов: цифры, буквы верхнего/нижнего регистра)
    password = fake.password(length=20, special_chars=False, 
                           digits=True, upper_case=True, lower_case=True)

    # 2. Получаем список пользователей до создания
    user_list_before = api_client.get_users()
    
    # 3. Создаем нового пользователя
    api_client.create_user(accountType, email, name, password)
    
    # 4. Получаем список пользователей после создания
    user_list_after = api_client.get_users()

    # 5. Проверяем увеличение количества пользователей
    with allure.step("Проверка увеличения количества пользователей"):
        assert len(user_list_after) - len(user_list_before) == 1, (
            f"Ожидалось увеличение на 1 пользователя. "
            f"Было: {len(user_list_before)}, стало: {len(user_list_after)}"
        )

    # 6. Получаем данные последнего созданного пользователя
    last_user = user_list_after[-1]

    # 7. Проверяем корректность данных пользователя
    with allure.step("Проверка данных созданного пользователя"):
        # Проверка имени
        assert last_user["name"] == name, (
            f"Несоответствие имени. Ожидалось: {name}, получено: {last_user['name']}"
        )
        # Проверка email
        assert last_user["email"] == email, (
            f"Несоответствие email. Ожидалось: {email}, получено: {last_user['email']}"
        )
        # Проверка типа аккаунта
        assert last_user["accountType"] == accountType, (
            f"Несоответствие типа аккаунта. "
            f"Ожидалось: {accountType}, получено: {last_user['accountType']}"
        )

@allure.title("Тест изменения имени и обращения пользователя")
def test_change_username(api_client: MafiaApi):
    """
    Тест проверяет функциональность изменения имени и обращения пользователя.
    Проверяет:
    1. Создание тестового пользователя
    2. Корректность изменения имени
    3. Корректность изменения обращения
    """
    
    # 1. Подготовка тестовых данных для создания пользователя
    accountType = "INDIVIDUAL"
    email = fake.email()  # Генерация случайного email
    initial_name = fake.name()  # Исходное имя пользователя
    password = fake.password(length=20, special_chars=False, 
                          digits=True, upper_case=True, lower_case=True)  # Сложный пароль

    # 2. Создание тестового пользователя
    with allure.step("Создание тестового пользователя"):
        api_client.create_user(accountType, email, initial_name, password)
    
    # 3. Получение списка пользователей
    with allure.step("Получение списка пользователей"):
        user_list = api_client.get_users()
        assert user_list, "Список пользователей пуст! Не удалось создать тестового пользователя"
    
    # 4. Получение ID последнего пользователя
    last_user = user_list[-1]
    user_id = last_user["id"]
    allure.attach(str(user_id), name="User ID", attachment_type=allure.attachment_type.TEXT)

    # 5. Подготовка новых данных
    new_name = fake.name()  # Новое имя для изменения
    pronouns = fake.prefix()  # Новое обращение
    allure.attach(f"Новые данные:\nИмя: {new_name}\nОбращение: {pronouns}", 
                 name="New User Data", 
                 attachment_type=allure.attachment_type.TEXT)

    # 6. Изменение данных пользователя
    with allure.step("Изменение имени и обращения пользователя"):
        api_client.edit_name_pronouns(user_id, new_name, pronouns)
    
    # 7. Получение обновленных данных
    with allure.step("Получение обновленных данных пользователя"):
        updated_user = api_client.get_user_by_ID(user_id)
        print(f"Обновленные данные пользователя: {updated_user}")
        allure.attach(str(updated_user), 
                     name="Updated User Data", 
                     attachment_type=allure.attachment_type.JSON)

    # 8. Проверки изменений
    with allure.step("Проверка изменений данных пользователя"):
        # Проверка имени
        assert updated_user["name"] == new_name, (
            f"Имя не было изменено корректно. "
            f"Ожидалось: {new_name}, Фактическое: {updated_user['name']}"
        )
        
        # Проверка обращения
        assert updated_user["pronouns"] == pronouns, (
            f"Обращение не было изменено корректно. "
            f"Ожидалось: {pronouns}, Фактическое: {updated_user['pronouns']}"
        )

@allure.title("Проверка статус-кода 401 при авторизации с невалидным паролем")
def test_negative_login_user_invalid_password(api_client: MafiaApi, test_data: DataProvider):
    """
    Тест проверяет, что при попытке авторизации с невалидным паролем
    возвращается статус-код 401 (Unauthorized) с соответствующим сообщением об ошибке.
    """
    # Получаем данные для INDIVIDUAL пользователя
    user_data = test_data.get("INDIVIDUAL")
    if not user_data:
        pytest.fail("Нет данных для INDIVIDUAL пользователя")

    email = user_data.get("email")
    valid_password = user_data.get("pass")
    invalid_password = valid_password + "не валидный"  # Делаем пароль невалидным

    with allure.step(f"Попытка авторизации с email {email} и невалидным паролем"):
        response = api_client.auth_user(email, invalid_password)
        print(f"Response: {response}")  # Для отладки

    # Проверка статус-кода (теперь response - это dict)
    with allure.step("Проверка статус-кода ответа"):
        status_code = response.get("statusCode") 
        assert status_code == 401, (
            f"Ожидался статус-код 401, но получен {status_code}. "
            f"Ответ сервера: {response}"
        )

    # Проверка сообщения об ошибке
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
    # 1. Получаем тестовые данные
    user_data = test_data.get("INDIVIDUAL")
    if not user_data:
        pytest.fail("Нет данных для INDIVIDUAL пользователя")

    # 2. Генерируем заведомо несуществующий email
    invalid_email = f"nonexistent_{fake.user_name()}@example.com"
    valid_password = user_data.get("pass")

    # 3. Попытка авторизации с неверным логином
    with allure.step(f"Попытка авторизации с несуществующим email {invalid_email}"):
        response = api_client.auth_user(invalid_email, valid_password)
        print(f"Response: {response}")  # Логирование для отладки

    # 4. Проверка статус-кода 404
    with allure.step("Проверка статус-кода ответа"):
        status_code = response.get("statusCode") 
        assert status_code == 404, (
            f"Ожидался статус-код 404 (Not Found), но получен {status_code}. "
            f"Полный ответ сервера: {response}"
        )

    # 5. Проверка сообщения об ошибке
    with allure.step("Проверка сообщения об ошибке"):
        error_message = response.get("message", "").lower()
        expected_phrases = ["not found", "user not exist", "не найден"]
        assert any(phrase in error_message for phrase in expected_phrases), (
            f"Ожидалось сообщение о ненайденном пользователе, но получено: {error_message}"
        )

@allure.title("Проверка создания пользователя с существующим email (ожидается 409 Conflict)")
def test_create_user_with_existing_email(api_client: MafiaApi, test_data: DataProvider):
    """
    Тест проверяет, что при попытке регистрации с уже существующим email
    возвращается статус 409 Conflict с соответствующим сообщением об ошибке.
    Проверяет:
    1. Статус код 409 в ответе
    2. Наличие сообщения о конфликте email
    3. Структуру ответа об ошибке
    """
    # 1. Получаем данные существующего пользователя
    user_data = test_data.get("INDIVIDUAL")
    if not user_data:
        pytest.fail("Нет данных для INDIVIDUAL пользователя в тестовых данных")

    # 2. Подготовка тестовых данных
    accountType = "INDIVIDUAL"
    existing_email = user_data.get("email")  # Берем email существующего пользователя
    name = fake.name()
    password = fake.password(length=20, special_chars=False, 
                           digits=True, upper_case=True, lower_case=True)

    # 3. Попытка создания пользователя с существующим email
    with allure.step(f"Попытка регистрации с email {existing_email}"):
        response = api_client.create_user(accountType, existing_email, name, password)
        
        # Логирование для отладки
        print(f"Response: {response}")
        allure.attach(str(response), name="API Response", attachment_type=allure.attachment_type.JSON)

     # 4. Проверка структуры ответа
    with allure.step("Проверка структуры ответа"):
        assert isinstance(response, dict), "Ответ должен быть словарем"
        assert "error" in response, "Ответ должен содержать поле 'error'"

    # 5. Проверка кода ошибки
    with allure.step("Проверка кода ошибки 409"):
        error_message = response["error"]
        assert "409" in error_message, (
            f"Ожидалась ошибка 409 Conflict, но получено: {error_message}"
        )

    # 6. Дополнительная проверка через прямой запрос
    with allure.step("Дополнительная проверка через GET запрос"):
        try:
            user_list = api_client.get_users()
            emails = [user["email"] for user in user_list]
            assert existing_email in emails, (
                f"Email {existing_email} не найден в списке пользователей после попытки повторной регистрации"
            )
        except Exception as e:
            pytest.fail(f"Ошибка при проверке списка пользователей: {str(e)}")