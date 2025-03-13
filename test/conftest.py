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