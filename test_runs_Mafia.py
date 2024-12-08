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
    ("qatests217@tester.com", "Qwerty1234!", "Qwerty1234!", "new_user3")
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
    ("qates@tester.com", "Qwerty1234!", "Qwerty1234!", "new_user3")
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
    sleep(7)
    signup_page.on_checkbox_community_guidelines()
    signup_page.click_button_continue()
    signup_page.click_button_continue_without_avatar()
    assert signup_page.is_username_displayed(user_name), f"Имя пользователя '{user_name}' не отображается на странице."