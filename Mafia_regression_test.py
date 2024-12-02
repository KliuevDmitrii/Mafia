from time import sleep
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.MainPage import MainPage
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
    

# @pytest.mark.parametrize("email, password", [
#     ("qa@test.com", "Qwerty1234!")
# ])
# def test_empty_fild(browser, email, password):
#     form_page = FormPage(browser)
#     form_page.