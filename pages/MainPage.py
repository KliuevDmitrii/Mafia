import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from configuration.ConfigProvider import ConfigProvider

class MainPage:
    """
    Этот класс предоставляет методы для выполнения действий на странице пользователя.
    """
     
    def __init__(self, driver: WebDriver) -> None:
        # Получение базового URL из конфигурации
        url = ConfigProvider().get("ui", "base_url")
        self.__url = url
        self.__driver = driver

    @allure.step("Перейти на главную страницу")
    def go(self):
        # Переход на главную страницу
        self.__driver.get(self.__url)

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        # Получение текущего URL страницы
        return self.__driver.current_url

    @allure.step("Страница пользователя открыта")
    def is_page_loaded(self):
        try:
            # Ожидание появления заголовка "Games on Ludio" на странице
            WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//h2[contains(@class, 'GamesTitle_g6v8k93') and text()='Games on Ludio']"))
            )
            return True
        except:
            return False
    
    @allure.step("Нажать на аватар пользователя")
    def click_avatar_user(self):
        time.sleep(3)  # Явное ожидание (нежелательно, лучше заменить WebDriverWait)
        # Ожидание появления аватара пользователя
        avatar_user = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '//div[@class="ProfileLinkWrapper_p2ot533"]//img[@alt="avatar"]'))
            )
        # Клик по аватару пользователя
        avatar_user.click()

    def is_div_element_name_user(self):
        """
        Проверяет, существует ли элемент div, содержащий изображение SVG.
        """
        try:
            # Поиск элемента div с указанными атрибутами
            self.__driver.find_element(By.XPATH, '//div[@width="100%" and @height="100%" and contains(@src, "data:image/svg+xml")]')
            return True
        except NoSuchElementException:
            return False