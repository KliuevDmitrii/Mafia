import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

class MainPage:
    """
    Этот класс предоставляет методы для выполнения действий на странице пользователя
    """
     
    def __init__(self, driver: WebDriver) -> None:
        self.__url = "https://dev.ludio.gg/"
        self.__driver = driver

    def get(self):
        self.__driver.get(self.__url)

    @allure.step("Страница пользователя открыта")
    def is_page_loaded(self):
        try:
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
        time.sleep(3)
        avatar_user = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '//div[@class="ProfileLinkWrapper_p2ot533"]//img[@alt="avatar"]'))
            )
        avatar_user.click()

    def is_div_element_name_user(self):
        try:
            self.__driver.find_element(By.XPATH, '//div[@width="100%" and @height="100%" and contains(@src, "data:image/svg+xml")]')
            return True
        except NoSuchElementException:
            return False