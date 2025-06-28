from time import sleep
import allure
import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.MainPage import MainPage
from pages.SignupPage import SignupPage
from pages.LoginPage import LoginPage
from pages.ResetPasswordPage import ResetPasswordPage
from pages.ProfilePage import ProfilePage
from pages.Stripe.CheckoutPage import CheckoutPage

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
def test_change_name(browser, test_data: dict):
    user_data = test_data.get("INDIVIDUAL")
    if not user_data:
        pytest.fail("Нет данных для INDIVIDUAL пользователя")

    email = user_data.get("email")
    password = user_data.get("pass")
    new_name = fake.name()

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

# Проверка добавления местоимения (ПАДАЕТ, надо думать)
@allure.id("Mafia-UI-5")
@allure.title("Добавление местоимения в профиль")
def test_add_pronouns(browser,  test_data: dict):
    user_data = test_data.get("INDIVIDUAL")
    if not user_data:
        pytest.fail("Нет данных для INDIVIDUAL пользователя")

    email = user_data.get("email")
    password = user_data.get("pass")
    pronouns = fake.prefix()

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

    with allure.step("Проверяем, что местоимение сохранено корректно"):
        assert pronouns == profile_page.check_user_pronouns(), "Новое местоимение не совпадает с введённым"

# Проверка создания нового персонального аккаунта без аватара
@allure.id("Mafia-UI-6.1")
@allure.title("Создание нового юзера с типом персональный без аватара")
def test_create_new_account_personal_without_avatar(browser):
    email = fake.email()
    password = fake.password(length=20, special_chars=True, digits=True, upper_case=True, lower_case=True)
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

    with allure.step("Проверить открытие Terms of Service в новой вкладке"):
        signup_page.click_terms_of_service_and_verify_new_tab()

    with allure.step("Проверить открытие Privacy Policy в новой вкладке"):
        signup_page.click_privacy_policy_and_verify_new_tab()

    with allure.step("Проверить открытие Community Guidelines в новой вкладке"):
        signup_page.click_community_guidelines_and_verify_new_tab()

    signup_page.click_button_continue()
    signup_page.click_button_continue_without_avatar()

    with allure.step("Проверить, что имя нового пользователя отображается на главной странице"):
        assert signup_page.is_username_displayed(user_name), f"Имя пользователя '{user_name}' не отображается на странице."

# Проверка создания нового персонального аккаунта с аватаром
@allure.id("Mafia-UI-6.2")
@allure.title("Создание нового юзера с типом персональный с аватаром")
def test_create_new_account_personal_with_avatar(browser):
    email = fake.email()
    password = fake.password(length=20, special_chars=True, digits=True, upper_case=True, lower_case=True)
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
@allure.id("Mafia-UI-7.1")
@allure.title("Создание нового юзера с типом организация без аватара")
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

    with allure.step("Проверить, что имя нового пользователя отображается на главной странице"):
        assert signup_page.is_username_displayed(user_name), f"Имя пользователя '{user_name}' не отображается на странице."

# Проверка регистрации с невалидным паролем
@allure.id("Mafia-UI-")
@allure.title("Регистрация с невалидным паролем (Faker)")
def test_negative_create_account_invalid_password_faker(browser):
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

# Проверка регистрации с невалидным паролем
@allure.id("Mafia-UI-")
@allure.title("Регистрация с невалидным паролем")
@pytest.mark.parametrize("password", [
    ("q"),
    ("qwert"),
    ("qwertyuiopasdfghjklla"),
    ("qwerty "),
    ("qwertyА123"),
    ("qwe rty")
])
def test_negative_create_account_invalid_password(browser, password):
    signup_page = SignupPage(browser)

    signup_page.go()
    signup_page.enter_password(password)

    with allure.step("Проверяем отображение ошибки валидации пароля"):
        assert signup_page.error_tooltip_password(), f"Ошибка валидации пароля '{password}' не отображается"

# Проверка регистрации с не совпадающими паролями
@allure.id("Mafia-UI-")
@allure.title("Регистрация с не совпадающими паролями")
def test_negative_create_account_password_not_match(browser):
    email = fake.email()
    password = fake.password(length=20, special_chars=True, digits=True, upper_case=True, lower_case=True)
    password_not_match = fake.password(length=20, special_chars=True, digits=True, upper_case=True, lower_case=True)

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

    with allure.step("Проверяем, что кнопка 'Login' не активна"):
        assert login_page.find_disabled_login_button(), "Кнопка Login не активна на странице"

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

    with allure.step("Проверяем, что кнопка 'Login' не активна"):
        assert login_page.find_disabled_login_button(), "Кнопка Login не активна на странице"

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
@allure.title("Сброс пароля")
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
@allure.title("Сброс пароля с несуществующим email")
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
@allure.title("Проверка активности кнопки сброса пароля при вводе не валидного  email")
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
@allure.title("Проверка совпадения введённого email с email на странице профиля юзера")
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
@allure.title("Проверка на количество оставшихся пропусков для нового юзера")
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

# Проверка на открытие новой вкладки для ввода данных банковской карты
@allure.id("")
@allure.title("Проверка открытия новой вкладки для ввода данных банковской карты")
def test_open_new_tab_strapi(browser):
    signup_page = SignupPage(browser)
    main_page = MainPage(browser)
    profile_page = ProfilePage(browser)
    
    
    email = fake.email()
    password = fake.password(length=20, special_chars=True, digits=True, upper_case=True, lower_case=True)
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
    main_page.click_avatar_user()
    profile_page.click_tab_billing_information()
    profile_page.subscription_plan_monthly()

    original_tabs = browser.window_handles 
    profile_page.click_button_continue()

    with allure.step("Ожидаем открытия новой вкладки со Stripe Checkout"):
        WebDriverWait(browser, 10).until(lambda drv: len(drv.window_handles) > len(original_tabs))

    new_tabs = browser.window_handles
    new_tab = list(set(new_tabs) - set(original_tabs))[0]
    
    with allure.step("Переключаемся на новую вкладку"):
        browser.switch_to.window(new_tab)

    with allure.step("Проверяем URL новой вкладки"):
        WebDriverWait(browser, 10).until(EC.url_contains("https://checkout.stripe.com/c/pay"))
        current_url = browser.current_url
        allure.attach(current_url, name="Stripe Checkout URL", attachment_type=allure.attachment_type.TEXT)
        assert current_url.startswith("https://checkout.stripe.com/c/pay"), \
            f"Ожидался переход на Stripe Checkout, но открыт: {current_url}"
        

@allure.id("")
@allure.title("Сравнение суммы месячной подписки на странице профиля и в Stripe Checkout")
def test_open_new_tab_strapi(browser):
    signup_page = SignupPage(browser)
    main_page = MainPage(browser)
    profile_page = ProfilePage(browser)
    checkout_page = CheckoutPage(browser)

    email = fake.email()
    password = fake.password(length=20, special_chars=True, digits=True, upper_case=True, lower_case=True)
    user_name = fake.name()

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

    main_page.click_avatar_user()
    profile_page.click_tab_billing_information()

    amount_from_profile = profile_page.get_subscription_amount_monthly()
    allure.attach(str(amount_from_profile), name="Сумма с profile_page", attachment_type=allure.attachment_type.TEXT)

    profile_page.subscription_plan_monthly()
    original_tabs = browser.window_handles
    profile_page.click_button_continue()

    with allure.step("Ожидаем открытия новой вкладки со Stripe Checkout"):
        WebDriverWait(browser, 10).until(lambda drv: len(drv.window_handles) > len(original_tabs))

    new_tab = list(set(browser.window_handles) - set(original_tabs))[0]

    with allure.step("Переключаемся на новую вкладку"):
        browser.switch_to.window(new_tab)

    with allure.step("Проверяем URL новой вкладки"):
        WebDriverWait(browser, 10).until(EC.url_contains("https://checkout.stripe.com/c/pay"))
        current_url = browser.current_url
        allure.attach(current_url, name="Stripe Checkout URL", attachment_type=allure.attachment_type.TEXT)
        assert current_url.startswith("https://checkout.stripe.com/c/pay"), \
            f"Ожидался переход на Stripe Checkout, но открыт: {current_url}"

    amount_from_stripe = checkout_page.get_subscription_amount()

    assert amount_from_profile == amount_from_stripe, (
        f"Сумма на странице профиля ({amount_from_profile}) "
        f"не совпадает с суммой на Stripe Checkout ({amount_from_stripe})"
    )

@allure.id("")
@allure.title("Сравнение суммы подписки на 3 месяца на странице профиля и в Stripe Checkout")
def test_open_new_tab_stripe_every_3_months(browser):
    signup_page = SignupPage(browser)
    main_page = MainPage(browser)
    profile_page = ProfilePage(browser)
    checkout_page = CheckoutPage(browser)

    email = fake.email()
    password = fake.password(length=20, special_chars=True, digits=True, upper_case=True, lower_case=True)
    user_name = fake.name()

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

    main_page.click_avatar_user()
    profile_page.click_tab_billing_information()

    # Получаем цену за месяц
    amount_from_profile = float(profile_page.get_subscription_amount_quarterly())
    allure.attach(str(amount_from_profile), name="Сумма с profile_page (в месяц)", attachment_type=allure.attachment_type.TEXT)

    # Выбираем план "каждые 3 месяца"
    profile_page.subscription_plan_every_3_months()
    original_tabs = browser.window_handles
    profile_page.click_button_continue()

    with allure.step("Ожидаем открытия новой вкладки со Stripe Checkout"):
        WebDriverWait(browser, 10).until(lambda drv: len(drv.window_handles) > len(original_tabs))

    new_tab = list(set(browser.window_handles) - set(original_tabs))[0]

    with allure.step("Переключаемся на новую вкладку"):
        browser.switch_to.window(new_tab)

    with allure.step("Проверяем URL новой вкладки"):
        WebDriverWait(browser, 10).until(EC.url_contains("https://checkout.stripe.com/c/pay"))
        current_url = browser.current_url
        allure.attach(current_url, name="Stripe Checkout URL", attachment_type=allure.attachment_type.TEXT)
        assert current_url.startswith("https://checkout.stripe.com/c/pay"), \
            f"Ожидался переход на Stripe Checkout, но открыт: {current_url}"

    # Получаем сумму из Stripe
    amount_from_stripe = checkout_page.get_subscription_amount()
    allure.attach(str(amount_from_stripe), name="Сумма со Stripe (за 3 месяца)", attachment_type=allure.attachment_type.TEXT)

    expected_amount = round(amount_from_profile * 3, 2)

    assert expected_amount == amount_from_stripe, (
        f"Ожидалась сумма {expected_amount} на Stripe, но получено {amount_from_stripe}"
    )


@allure.id("")
@allure.title("Сравнение суммы годовой подписки на странице профиля и в Stripe Checkout")
def test_open_new_tab_stripe_annual(browser):
    signup_page = SignupPage(browser)
    main_page = MainPage(browser)
    profile_page = ProfilePage(browser)
    checkout_page = CheckoutPage(browser)

    email = fake.email()
    password = fake.password(length=20, special_chars=True, digits=True, upper_case=True, lower_case=True)
    user_name = fake.name()

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

    main_page.click_avatar_user()
    profile_page.click_tab_billing_information()

    # Получаем сумму за месяц на профиле
    amount_from_profile = float(profile_page.get_subscription_amount_annual())
    allure.attach(str(amount_from_profile), name="Сумма с profile_page (в месяц)", attachment_type=allure.attachment_type.TEXT)

    # Выбираем годовую подписку
    profile_page.subscription_plan_annual()
    original_tabs = browser.window_handles
    profile_page.click_button_continue()

    with allure.step("Ожидаем открытия новой вкладки со Stripe Checkout"):
        WebDriverWait(browser, 10).until(lambda drv: len(drv.window_handles) > len(original_tabs))

    new_tab = list(set(browser.window_handles) - set(original_tabs))[0]

    with allure.step("Переключаемся на новую вкладку"):
        browser.switch_to.window(new_tab)

    with allure.step("Проверяем URL новой вкладки"):
        WebDriverWait(browser, 10).until(EC.url_contains("https://checkout.stripe.com/c/pay"))
        current_url = browser.current_url
        allure.attach(current_url, name="Stripe Checkout URL", attachment_type=allure.attachment_type.TEXT)
        assert current_url.startswith("https://checkout.stripe.com/c/pay"), \
            f"Ожидался переход на Stripe Checkout, но открыт: {current_url}"

    amount_from_stripe = checkout_page.get_subscription_amount()
    allure.attach(str(amount_from_stripe), name="Сумма со Stripe (в год)", attachment_type=allure.attachment_type.TEXT)

    expected_annual = round(amount_from_profile * 12, 2)

    assert expected_annual == amount_from_stripe, (
        f"Ожидалась сумма {expected_annual} на Stripe, но получено {amount_from_stripe}"
    )


# Оформление месячной подписки
@allure.id("")
@pytest.mark.parametrize("card_number, expiry_date, cvc, name_placeholder", [
    ("4242424242424242", "12/25", "123", "Test User")
])
@allure.title("Оформление месячной подписки")
def test_monthly_subscription(browser, card_number, expiry_date, cvc, name_placeholder):
    signup_page = SignupPage(browser)
    main_page = MainPage(browser)
    profile_page = ProfilePage(browser)
    checkout_page = CheckoutPage(browser)
    
    email = fake.email()
    password = fake.password(length=20, special_chars=True, digits=True, upper_case=True, lower_case=True)
    user_name = fake.name()    

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
    
    main_page.click_avatar_user()
    profile_page.click_tab_billing_information()
    
    profile_page.subscription_plan_monthly()
    original_tabs = browser.window_handles
    profile_page.click_button_continue()

    # Переход в новую вкладку Stripe Checkout
    WebDriverWait(browser, 10).until(lambda drv: len(drv.window_handles) > len(original_tabs))
    new_tab = list(set(browser.window_handles) - set(original_tabs))[0]
    browser.switch_to.window(new_tab)

    checkout_page.select_payment_method_card()

    # Ввод реквизитов карты
    checkout_page.enter_card_details(
        card_number=card_number,
        expiry_date=expiry_date,
        cvc=cvc,
        placeholder=name_placeholder
    )
    checkout_page.click_submit_button()
    sleep(5)