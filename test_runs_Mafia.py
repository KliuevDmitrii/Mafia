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

@pytest.mark.parametrize("email, password, confirm_password, user_name", [
    ("qatests33@tester.com", "Qwerty1234!", "Qwerty1234!", "new_user3")
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
    signup_page.account_tipe_personal()
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
    signup_page.account_tipe_personal()
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
    signup_page.account_tipe_organization()
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
    ("qa@tester.com ", "Qwerty1234!")
])
def test_invalid_email(browser, email):
    login_page = LoginPage(browser)
    login_page.get()
    login_page.enter_email(email)
    error_text = login_page.invalid_email_format()
    
    assert error_text == "Invalid Email Format", f"Ожидали текст ошибки 'Invalid Email Format', получили '{error_text}'"

@pytest.mark.parametrize("email, password", [
    ("qa@@tester.com", "Qwerty1234!")
])
def test_login_user_invalid_email(browser, email, password):
    login_page = LoginPage(browser)
    login_page.get()
    login_page.enter_email(email)
    login_page.enter_password(password)

    assert login_page.find_disabled_login_button(), "Кнопка Login не активна на странице"
