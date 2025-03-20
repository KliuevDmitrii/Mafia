from time import sleep
import allure
import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.MainPage import MainPage
from pages.SignupPage import SignupPage
from pages.LoginPage import LoginPage
from pages.ResetPasswordPage import ResetPasswordPage
from pages.ProfilePage import ProfilePage

fake = Faker()


# Проверка открытия страницы
@allure.id("Mafia-UI-1")
@allure.title("Загрузка главной страницы")
def test_open_page(browser):
    main_page = MainPage(browser)
    main_page.go()

    with allure.step("Проверить, что главная страница загружается"):
        assert main_page.is_page_loaded(), "Элемент с текстом 'Games on Ludio' не найден на странице."

# Проверка авторизация зарегестрированного пользователя
@allure.id("Mafia-UI-2.1")
@allure.title("Авторизация зарегестрированного пользователя с типом персональный")
def auth_user_individual_test(browser, test_data: dict):
    user_data = test_data.get("INDIVIDUAL")
    if not user_data:
        pytest.fail("Нет данных для INDIVIDUAL пользователя")

    email = user_data.get("email")
    password = user_data.get("pass")

    login_page = LoginPage(browser)
    main_page = MainPage(browser)
    login_page.go()
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_button_log_in()

    with allure.step("Проверить, что пользователь авторизовался"):
        assert main_page.is_div_element_name_user, "Имя пользователя отсутствует на странице"

# Проверка авторизация зарегестрированного пользователя
@allure.id("Mafia-UI-2.2")
@allure.title("Авторизация зарегестрированного пользователя с типом организация")
def auth_user_org_test(browser, test_data: dict):
    user_data = test_data.get("ORGANIZATION")
    if not user_data:
        pytest.fail("Нет данных для ORGANIZATION пользователя")

    email = user_data.get("email")
    password = user_data.get("pass")

    login_page = LoginPage(browser)
    main_page = MainPage(browser)
    login_page.go()
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_button_log_in()

    with allure.step("Проверить, что пользователь авторизовался"):
        assert main_page.is_div_element_name_user, "Имя пользователя отсутствует на странице"
    

# Проверка выхода из профиля
@allure.id("Mafia-UI-3")
@allure.title("Выход из аккаунта зарегестрированного пользователя")
def test_log_out_user(browser, test_data: dict):
    user_data = test_data.get("INDIVIDUAL")
    if not user_data:
        pytest.fail("Нет данных для INDIVIDUAL пользователя")

    email = user_data.get("email")
    password = user_data.get("pass")
    login_page = LoginPage(browser)
    login_page.go()
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_button_log_in()
    login_page.click_button_log_out()

    with allure.step("Проверить, что пользователь выполнил разлогин"):
        assert login_page.click_new_call_button(), "Кнопка нового звонка присутствует на странице"

# Проверка смены имени (ПАДАЕТ, надо думать)
@allure.id("Mafia-UI-4")
@allure.title("Смена имени зарегестрированного пользователя")
@pytest.mark.parametrize("email, password, new_name", [
    ("qa@tester.com", "Qwerty1234!", "TEST1")
])
def test_change_name(browser, email, password, new_name):
    login_page = LoginPage(browser)
    main_page = MainPage(browser)
    profile_page = ProfilePage(browser)
    login_page.go()
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_button_log_in()
    main_page.click_avatar_user()
    profile_page.click_button_edit()
    profile_page.input_name(new_name)
    profile_page.click_button_save()

    assert new_name == profile_page.check_user_name(), "Новое имя в профиле не совпадает с введенным"

# Проверка добавления местоимения
@pytest.mark.parametrize("email, password, pronouns", [
    ("qa@tester.com", "Qwerty1234!", "He")
])
def test_add_pronouns(browser, email, password, pronouns):
    login_page = LoginPage(browser)
    main_page = MainPage(browser)
    profile_page = ProfilePage(browser)
    login_page.go()
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_button_log_in()
    main_page.click_avatar_user()
    profile_page.click_button_edit()
    profile_page.input_pronouns(pronouns)
    profile_page.click_button_save()

    assert pronouns == profile_page.check_user_pronouns(), "Новое местоимение не совпадает с введённым"

# Проверка создания нового персонального аккаунта без аватара
def test_create_new_account_personal_without_avatar(browser):
    email = fake.email()
    password = fake.password(length=20, special_chars=False, digits=True, upper_case=True, lower_case=True)
    user_name = fake.name()    

    signup_page = SignupPage(browser)

    signup_page.go()
    signup_page.enter_email(email)
    signup_page.enter_password(password)
    signup_page.confirm_password(password)
    signup_page.click_button_create_account()
    signup_page.choose_username(user_name)
    signup_page.account_type_personal()
    signup_page.on_checkbox_privacy_policy()
    signup_page.on_checkbox_community_guidelines()
    signup_page.click_button_continue()
    signup_page.click_button_continue_without_avatar()

    with allure.step("Проверить, что имя нового пользователя отображается на главной странице"):
        assert signup_page.is_username_displayed(user_name), f"Имя пользователя '{user_name}' не отображается на странице."

# Проверка создания нового персонального аккаунта с аватаром
def test_create_new_account_personal_with_avatar(browser):
    email = fake.email()
    password = fake.password(length=20, special_chars=False, digits=True, upper_case=True, lower_case=True)
    user_name = fake.name()
    avatar_path = '/home/dmitriik/Документы/Mafia/avatar.png'

    signup_page = SignupPage(browser)

    signup_page.go()
    signup_page.enter_email(email)
    signup_page.enter_password(password)
    signup_page.confirm_password(password)
    signup_page.click_button_create_account()
    signup_page.choose_username(user_name)
    signup_page.account_type_personal()
    signup_page.on_checkbox_privacy_policy()
    signup_page.on_checkbox_community_guidelines()
    signup_page.click_button_continue()
    signup_page.add_avatar_photo(avatar_path)
    signup_page.click_button_continue_step_2()

    with allure.step("Проверить, что имя нового пользователя отображается на главной странице"):
        assert signup_page.is_username_displayed(user_name), f"Имя пользователя '{user_name}' не отображается на странице."
    
# Проверка создание аккаунта с типом организация без аватара    
def test_create_new_account_organization_without_avatar(browser):
    email = f"{fake.user_name()}@hi2.in"
    user_name = fake.name()
    password = fake.password(length=20, special_chars=False, digits=True, upper_case=True, lower_case=True)

    signup_page = SignupPage(browser)
    signup_page.go()
    signup_page.enter_email(email)
    signup_page.enter_password(password)
    signup_page.confirm_password(password)
    signup_page.click_button_create_account()
    signup_page.choose_username(user_name)
    signup_page.on_checkbox_privacy_policy()
    signup_page.on_checkbox_community_guidelines()
    signup_page.click_button_continue()
    signup_page.click_button_continue_without_avatar()

    assert signup_page.is_username_displayed(user_name), f"Имя пользователя '{user_name}' не отображается на странице."

# Проверка регистрации с невалидным паролем
@allure.id("Mafia-UI-")
@allure.title("Регистрация с невалидным паролем")
def test_negative_create_account_invalid_password(browser):
    invalid_passwords = [
    fake.pystr(min_chars=1, max_chars=5),
    fake.pystr(min_chars=21, max_chars=25),
    fake.password(length=8) + " ",
    "пароль123!",
    fake.numerify(text="#" * 8),
    fake.pystr(min_chars=6, max_chars=20).upper(),
    fake.pystr(min_chars=6, max_chars=20).lower()
    ]

    signup_page = SignupPage(browser)
    signup_page.go()
    signup_page.enter_password(invalid_passwords)

    with allure.step("Проверяем отображение ошибки валидации пароля"):
        assert signup_page.error_tooltip_password(), "Ошибка валидации пароля не отображается"

# Проверка регистрации с не совпадающими паролями
@allure.id("Mafia-UI-")
@allure.title("Регистрация с не совпадающими паролями")
def test_negative_create_account_password_not_match(browser):
    email = fake.email()
    password = fake.password(length=20, special_chars=False, digits=True, upper_case=True, lower_case=True)
    password_not_match = fake.password(length=20, special_chars=False, digits=True, upper_case=True, lower_case=True)

    signup_page = SignupPage(browser)

    signup_page.go()
    signup_page.enter_email(email)
    signup_page.enter_password(password)
    signup_page.confirm_password(password_not_match)
    signup_page.click_button_create_account()

    with allure.step("Проверяем, что заголовок 'Create an account' остается на странице"):
        assert signup_page.is_create_account_header_displayed(), "Заголовок 'Create an account' отсутствует, значит, произошел переход"


# Проверка отображения текста о не валидном email при авторизации
@allure.id("Mafia-UI-")
@allure.title("Отображение ошибки при вводе не валидного email")
@pytest.mark.parametrize("email", [
    ("qa@tester", "Qwerty1234!"),  # Нет доменной зоны
    ("qatester.com", "Qwerty1234!"),  # Нет @
    ("qa@@tester.com", "Qwerty1234!"),  # Двойной @
    ("qа@tester.com", "Qwerty1234!"),  # Кириллический символ "а"
    ("q", "Qwerty1234!"),  # Односимвольный email
    ("qa@tester.com ", "Qwerty1234!"),  # Пробел в конце
    ("", "Qwerty1234!"),  # Пустая строка
    (" qa@tester.com", "Qwerty1234!"),  # Пробел в начале
    ("@tester.com", "Qwerty1234!"),  # Нет локальной части
    ("qa@", "Qwerty1234!"),  # Нет домена
    ("qa@testercom", "Qwerty1234!"),  # Нет точки в домене
    ("qa..tester@tester.com", "Qwerty1234!"),  # Двойная точка
    ("qa!#%&*{}[]/=?^`+@tester.com", "Qwerty1234!"),  # Спецсимволы
    ("тест@tester.com", "Qwerty1234!"),  # Кириллица в email
    ("qa @tester.com", "Qwerty1234!"),  # Пробел внутри
    ("qa\t@tester.com", "Qwerty1234!"),  # Табуляция внутри
    ("qa@tester,com", "Qwerty1234!"),  # Запятая вместо точки
    ("a" * 250 + "@tester.com", "Qwerty1234!"),  # Длинный email
    ("qa@tester.", "Qwerty1234!"),  # Нет доменного суффикса
    ("qa@tester..com", "Qwerty1234!"),  # Двойной суффикс
    ('"qa"@tester.com', "Qwerty1234!"),  # Кавычки в локальной части
    ("qa😀@tester.com", "Qwerty1234!"),  # Эмодзи в email
])
def test_invalid_email(browser, email):
    login_page = LoginPage(browser)
    login_page.go()
    login_page.enter_email(email)
    error_text = login_page.invalid_email_format()
    
    with allure.step("Проверяем отображение ошибки"):
        assert error_text == "Invalid Email Format", f"Ожидали текст ошибки 'Invalid Email Format', получили '{error_text}'"

@allure.id("Mafia-UI-")
@allure.title("Авторизация со случайным невалидным email (Faker)")
def test_invalid_email_faker(browser):
    login_page = LoginPage(browser)
    invalid_email = login_page.generate_invalid_email()
    login_page.go()
    
    with allure.step(f"Вводим случайный невалидный email: {invalid_email}"):
        login_page.enter_email(invalid_email)
    
    with allure.step("Проверяем отображение ошибки"):
        error_text = login_page.invalid_email_format()
        assert error_text == "Invalid Email Format", f"Ожидали 'Invalid Email Format', получили '{error_text}'"

# Проверка авторизации с невалидным email
@allure.id("Mafia-UI-InvalidEmailLogin")
@allure.title("Авторизация с невалидным email, кнопка 'Login' не активна")
@pytest.mark.parametrize("email, password", [
    ("qa@tester", "Qwerty1234!"),  # Нет доменной зоны
    ("qatester.com", "Qwerty1234!"),  # Нет @
    ("qa@@tester.com", "Qwerty1234!"),  # Двойной @
    ("qа@tester.com", "Qwerty1234!"),  # Кириллический символ "а"
    ("q", "Qwerty1234!"),  # Односимвольный email
    ("qa@tester.com ", "Qwerty1234!"),  # Пробел в конце
    ("", "Qwerty1234!"),  # Пустая строка
    (" qa@tester.com", "Qwerty1234!"),  # Пробел в начале
    ("@tester.com", "Qwerty1234!"),  # Нет локальной части
    ("qa@", "Qwerty1234!"),  # Нет домена
    ("qa@testercom", "Qwerty1234!"),  # Нет точки в домене
    ("qa..tester@tester.com", "Qwerty1234!"),  # Двойная точка
    ("qa!#%&*{}[]/=?^`+@tester.com", "Qwerty1234!"),  # Спецсимволы
    ("тест@tester.com", "Qwerty1234!"),  # Кириллица в email
    ("qa @tester.com", "Qwerty1234!"),  # Пробел внутри
    ("qa\t@tester.com", "Qwerty1234!"),  # Табуляция внутри
    ("qa@tester,com", "Qwerty1234!"),  # Запятая вместо точки
    ("a" * 250 + "@tester.com", "Qwerty1234!"),  # Длинный email
    ("qa@tester.", "Qwerty1234!"),  # Нет доменного суффикса
    ("qa@tester..com", "Qwerty1234!"),  # Двойной суффикс
    ('"qa"@tester.com', "Qwerty1234!"),  # Кавычки в локальной части
    ("qa😀@tester.com", "Qwerty1234!"),  # Эмодзи в email
])
def test_login_user_invalid_email(browser, email, password):
    login_page = LoginPage(browser)
    login_page.go()

    with allure.step(f"Вводим email: {email}"):
        login_page.enter_email(email)

    with allure.step(f"Вводим пароль: {password}"):
        login_page.enter_password(password)

    with allure.step("Проверяем, что кнопка 'Login' не активна"):
        assert login_page.find_disabled_login_button(), "Кнопка Login не активна на странице"

# Проверка сброса пароля
@pytest.mark.parametrize("email", [
    ("qa@tester.com")
])
def test_positive_reset_password(browser, email):
    reset_page = ResetPasswordPage(browser)
    reset_page.go()
    reset_page.forgot_password()
    reset_page.enter_email(email)
    reset_page.click_button_reset_password()

    assert reset_page.popup() == "We have sent you instructions to change your password by email.", "Инструкция не отправлена на указанный email"

# Проверка popup с информацией о невалидым email при сбросе пароля
@pytest.mark.parametrize("email", [
    ("qa@tester.co")
])
def test_negative_reset_password_not_user_email(browser, email):
    reset_page = ResetPasswordPage(browser)
    reset_page.go()
    reset_page.forgot_password()
    reset_page.enter_email(email)
    reset_page.click_button_reset_password()

    assert reset_page.popup_alert()

# Проверка активности кнопки сброса пароля при вводе не валидного  email
@pytest.mark.parametrize("email", [
    ("qa@testercom"),
    ("qa@@tester.com"),
    ("qа@tester.com"),
    ("@tester.com"),
    (("qatester.com"))
])
def test_negative_reset_password_invalid_email(browser, email):
    reset_page = ResetPasswordPage(browser)
    reset_page.go()
    reset_page.forgot_password()
    reset_page.enter_email(email)

    assert reset_page.button_reset_password_disabled(), "Кнопка сброса пароля активна после ввода невалидного email"

# Проверка совпадения введённого email с email на странице профиля юзера
@pytest.mark.parametrize("email, password", [
    ("qa@tester.com", "Qwerty1234!")
])
def test_open_profile_user(browser, email, password):
    login_page = LoginPage(browser)
    main_page = MainPage(browser)
    profile_page = ProfilePage(browser)
    login_page.go()
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_button_log_in()
    main_page.click_avatar_user()

    assert email == profile_page.check_user_email(), "Email в профиле не совпадает с введенным"

# Проверка на количество оставшихся пропусков для нового юзера
@pytest.mark.parametrize("email, password, confirm_password, user_name", [
    ("qate2347sts3@ozester.com", "Qwerty12345!", "Qwerty12345!", "new")
])
def test_remaining_passes_for_new_user(browser, email, password, confirm_password, user_name):
    signup_page = SignupPage(browser)
    main_page = MainPage(browser)
    profile_page = ProfilePage(browser)
    signup_page.go()
    signup_page.enter_email(email)
    signup_page.enter_password(password)
    signup_page.confirm_password(confirm_password)
    signup_page.click_button_create_account()
    signup_page.choose_username(user_name)
    signup_page.account_type_personal()
    signup_page.on_checkbox_privacy_policy()
    signup_page.on_checkbox_community_guidelines()
    signup_page.click_button_continue()
    signup_page.click_button_continue_without_avatar()
    main_page.click_avatar_user()
    profile_page.click_tab_billing_information()
    remaining_passes_text = profile_page.check_remaining_passes()
    
    assert remaining_passes_text is not None, "Не удалось получить текст оставшихся пропусков"
    assert remaining_passes_text.isdigit(), f"Текст '{remaining_passes_text}' не является числом"
    print(f"Оставшиеся пропуски: {remaining_passes_text}")

# Проверка на добавление банковской карты для для нового пользователя
@pytest.mark.parametrize("email, password, confirm_password, user_name, card_number, card_date, card_cvc, cardholder_name", [
    ("qate235@teyte.kn", "Qwerty12345!", "Qwerty12345!", "new", 4242424242424242, 1234, 123, "Test User")
])
def test_add_credit_card(browser, email, password, confirm_password, user_name, card_number, card_date, card_cvc, cardholder_name):
    signup_page = SignupPage(browser)
    main_page = MainPage(browser)
    profile_page = ProfilePage(browser)
    signup_page.go()
    signup_page.create_new_accaunt()
    signup_page.enter_email(email)
    signup_page.enter_password(password)
    signup_page.confirm_password(confirm_password)
    signup_page.click_button_create_account()
    signup_page.choose_username(user_name)
    signup_page.account_type_personal()
    signup_page.on_checkbox_privacy_policy()
    signup_page.on_checkbox_community_guidelines()
    signup_page.click_button_continue()
    signup_page.click_button_continue_without_avatar()
    main_page.click_avatar_user()
    profile_page.click_tab_billing_information()
    profile_page.click_button_update()
    profile_page.subscription_plan_monthly()
    profile_page.click_button_continue()
    profile_page.add_card(card_number, card_date, card_cvc, cardholder_name)
    profile_page.click_button_start_my_subscription()
    profile_page.click_button_confirm()
    expected_last_four_digits = card_number[-4:]
    is_valid = profile_page.check_new_card_add(expected_last_four_digits)
    
    assert is_valid, f"Ожидаемые последние 4 цифры: {expected_last_four_digits}, но отображается другая информация"




