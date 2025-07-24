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

from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
        data_provider.get_stripe_token(),
        data_provider.get_stripe_key()
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

@pytest.fixture
def card_data():
    raw = DataProvider().get_card_data("default")
    raw["exp_month"] = int(raw["exp_month"])
    raw["exp_year"] = int(raw["exp_year"])
    return raw

@pytest.fixture(scope="session")
def db_session():
    """
    Создаёт сессию SQLAlchemy с туннелем SSH для доступа к PostgreSQL.
    """
    config = ConfigProvider()

    ssh_host = config.get_ssh_host()
    ssh_port = config.get_ssh_port()
    ssh_username = config.get_ssh_username()
    ssh_password = config.get_ssh_password()
    db_url = config.get_db_connection_string()

    assert all([ssh_host, ssh_port, ssh_username, ssh_password, db_url]), "Неполные настройки SSH или DB"

    # Параметры из строки подключения
    import re
    match = re.search(r"@([^:/]+):(\d+)/", db_url)
    assert match, "Не удалось распарсить хост и порт из строки подключения"
    remote_host = match.group(1)
    remote_port = int(match.group(2))

    with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_username,
        ssh_password=ssh_password,
        remote_bind_address=(remote_host, remote_port),
        local_bind_address=("127.0.0.1",),
    ) as tunnel:
        local_port = tunnel.local_bind_port
        updated_url = db_url.replace(f"{remote_host}:{remote_port}", f"127.0.0.1:{local_port}")

        engine = create_engine(updated_url)
        Session = sessionmaker(bind=engine)
        session = Session()

        yield session

        session.close()
        engine.dispose()