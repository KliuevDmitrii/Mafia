from socket import timeout
import pytest
import allure

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from configuration.ConfigProvider import ConfigProvider
from testdata.DataProvider import DataProvider
from api.MafiaApi import MafiaApi

@pytest.fixture
def browser():
    with allure.step("Открыть и настроить браузер"):
        config = ConfigProvider()
        timeout = config.getint("ui", "timeout")

        browser_name = config.get("ui", "browser_name", fallback="chrome")
        browser_name = browser_name.lower() if browser_name else "chrome"

        if browser_name == 'chrome':
            browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        elif browser_name in ['ff', 'firefox']:
            browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        else:
            raise ValueError(f"Неизвестное значение browser_name: {browser_name}")

        browser.implicitly_wait(timeout)
        browser.maximize_window()

    yield browser

    with allure.step("Закрыть браузер"):
            browser.quit()

@pytest.fixture
def test_data():
        return DataProvider()

@pytest.fixture
def api_client() -> MafiaApi:
    config = ConfigProvider()
    data_provider = DataProvider()
    return MafiaApi(
        config.get("api", "base_url"),
        data_provider.get_token()
    )

@pytest.fixture
def authorized_api_client():
    config = ConfigProvider()
    data_provider = DataProvider()

    base_url = config.get("api", "base_url")
    email = data_provider.get("INDIVIDUAL")["email"]
    password = data_provider.get("INDIVIDUAL")["pass"]

    temp_api = MafiaApi(base_url, token="")

    with allure.step("Авторизация INDIVIDUAL пользователя через API"):
        auth_response = temp_api.auth_user(email, password)

        if "accessToken" not in auth_response:
            raise Exception(f"Авторизация не удалась: {auth_response}")

        token = auth_response["accessToken"]

    return MafiaApi(base_url, token=token)