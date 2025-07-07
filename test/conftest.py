from socket import timeout
import pytest
import allure

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from configuration.ConfigProvider import ConfigProvider
from testdata.DataProvider import DataProvider
from api.MafiaApi import MafiaApi
from api.StripeApi import StripeApi

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def browser():
    with allure.step("Открыть и настроить браузер"):
        config = ConfigProvider()
        timeout = config.getint("ui", "timeout")

        browser_name = config.get("ui", "browser_name", fallback="chrome")
        browser_name = browser_name.lower() if browser_name else "chrome"

        if browser_name == 'chrome':
            options = webdriver.ChromeOptions()
            browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        elif browser_name in ['ff', 'firefox']:
            options = webdriver.FirefoxOptions()
            browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

        elif browser_name == 'edge':
            options = webdriver.EdgeOptions()
            browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

        elif browser_name == 'brave':
            options = webdriver.ChromeOptions()
            brave_path = config.get("ui", "brave_path", fallback="/usr/bin/brave-browser")
            options.binary_location = brave_path
            browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

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

@pytest.fixture
def stripe_api():
    config = ConfigProvider()
    data_provider = DataProvider()
    stripe_url = config.get("api", "base_stripe_url")

    assert stripe_url, "base_stripe_url не найден в test_config.ini"

    return StripeApi(
        stripe_url,
        data_provider.get_stripe_token()
    )

@pytest.fixture
def annual_price_id():
    return DataProvider().get_annual_price_id()

@pytest.fixture
def month_price_id():
    return DataProvider().get_month_price_id()

@pytest.fixture
def quarter_price_id():
    return DataProvider().get_quarter_price_id()

@pytest.fixture
def every_day_price_id():
    return DataProvider().get_every_day_price_id()