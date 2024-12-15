from time import sleep
import pytest
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

@pytest.fixture
def browser():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_open_page(browser):
    main_page = MainPage(browser)
    main_page.get()

    assert main_page.is_page_loaded(), "Элемент с текстом 'Games on Ludio' не найден на странице."
    

@pytest.mark.parametrize("email, password", [
    ("qa@tester.com", "Qwerty1234!")
])
def test_login_user(browser, email, password):
    login_page = LoginPage(browser)
    login_page.get()
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_button_log_in()

    assert login_page.click_new_call_button(), "Кнопка New Call отсутствует на странице"

@pytest.mark.parametrize("email, password", [
    ("qa@tester.com", "Qwerty1234!")
])
def test_log_out_user(browser, email, password):
    login_page = LoginPage(browser)
    login_page.get()
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_button_log_in()
    login_page.click_button_log_out()

    assert login_page.click_new_call_button(), "Кнопка нового звонка присутствует на странице"


@pytest.mark.parametrize("email, password, confirm_password, user_name", [
    ("qate234sts33@tes34ter.com", "Qwerty12345!", "Qwerty12345!", "new")
])
def test_create_new_account_personal_without_avatar(browser, email, password, confirm_password, user_name):
    signup_page = SignupPage(browser)
    signup_page.get()
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

    assert signup_page.is_username_displayed(user_name), f"Имя пользователя '{user_name}' не отображается на странице."

@pytest.mark.parametrize("email, password, confirm_password, user_name", [
    ("qatests2617@tester.com", "Qwerty1234!", "Qwerty1234!", "new_user3")
])
def test_create_new_account_personal_with_avatar(browser, email, password, confirm_password, user_name):
    signup_page = SignupPage(browser)
    signup_page.get()
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
    avatar_path = '/home/dmitriik/Документы/Mafia/avatar.png'
    signup_page.add_avatar_photo(avatar_path)
    signup_page.click_button_continue_step_2()

    assert signup_page.is_username_displayed(user_name), f"Имя пользователя '{user_name}' не отображается на странице."
    
@pytest.mark.parametrize("email, password, confirm_password, user_name", [
    ("qates43@tester.com", "Qwerty1234!", "Qwerty1234!", "new_user3")
])
def test_create_new_account_organization_without_avatar(browser, email, password, confirm_password, user_name):
    signup_page = SignupPage(browser)
    signup_page.get()
    signup_page.create_new_accaunt()
    signup_page.enter_email(email)
    signup_page.enter_password(password)
    signup_page.confirm_password(confirm_password)
    signup_page.click_button_create_account()
    signup_page.choose_username(user_name)
    signup_page.account_type_organization()
    signup_page.on_checkbox_privacy_policy()
    signup_page.on_checkbox_community_guidelines()
    signup_page.click_button_continue()
    signup_page.click_button_continue_without_avatar()

    assert signup_page.is_username_displayed(user_name), f"Имя пользователя '{user_name}' не отображается на странице."

@pytest.mark.parametrize("email, password", [
    ("qa@tester", "Qwerty1234!"),
    ("qatester.com", "Qwerty1234!"),
    ("qa@@tester.com", "Qwerty1234!"),
    ("qа@tester.com", "Qwerty1234!"),
    ("q", "Qwerty1234!"),
    ("qa@tester.com ", "Qwerty1234!"),
    ("", "Qwerty1234!")
])
def test_invalid_email(browser, email):
    login_page = LoginPage(browser)
    login_page.get()
    login_page.enter_email(email)
    error_text = login_page.invalid_email_format()
    
    assert error_text == "Invalid Email Format", f"Ожидали текст ошибки 'Invalid Email Format', получили '{error_text}'"

@pytest.mark.parametrize("email, password", [
    ("qa@@tester.com", "Qwerty1234!"),
    ("qa@tester.com ", "")
])
def test_login_user_invalid_email(browser, email, password):
    login_page = LoginPage(browser)
    login_page.get()
    login_page.enter_email(email)
    login_page.enter_password(password)

    assert login_page.find_disabled_login_button(), "Кнопка Login не активна на странице"

@pytest.mark.parametrize("email", [
    ("qa@tester.com")
])
def test_positive_reset_password(browser, email):
    reset_page = ResetPasswordPage(browser)
    reset_page.get()
    reset_page.forgot_password()
    reset_page.enter_email(email)
    reset_page.click_button_reset_password()

    assert reset_page.popup() == "We have sent you instructions to change your password by email.", "Инструкция не отправлена на указанный email"

@pytest.mark.parametrize("email", [
    ("qa@tester.co")
])
def test_negative_reset_password_not_user_email(browser, email):
    reset_page = ResetPasswordPage(browser)
    reset_page.get()
    reset_page.forgot_password()
    reset_page.enter_email(email)
    reset_page.click_button_reset_password()

    assert reset_page.popup_alert()

@pytest.mark.parametrize("email", [
    ("qa@testercom"),
    ("qa@@tester.com"),
    ("qа@tester.com"),
    ("@tester.com"),
    (("qatester.com"))
])
def test_negative_reset_password_invalid_email(browser, email):
    reset_page = ResetPasswordPage(browser)
    reset_page.get()
    reset_page.forgot_password()
    reset_page.enter_email(email)

    assert reset_page.button_reset_password_disabled(), "Кнопка сброса пароля активна после ввода невалидного email"

@pytest.mark.parametrize("email, password", [
    ("qa@tester.com", "Qwerty1234!")
])
def test_open_profile_user(browser, email, password):
    login_page = LoginPage(browser)
    main_page = MainPage(browser)
    profile_page = ProfilePage(browser)
    login_page.get()
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_button_log_in()
    main_page.click_name_user()

    assert email == profile_page.check_user_email(), "Email в профиле не совпадает с введенным"
