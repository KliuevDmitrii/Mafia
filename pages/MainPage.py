import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainPage:
    """
    Этот класс предоставляет методы для выполнения действий на странице пользователя
    """
     
    def __init__(self, driver):
        self._driver = driver

    def get(self):
        self._driver.get("https://dev.ludio.gg/")

    def is_page_loaded(self):
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//h2[contains(@class, 'GamesTitle_g6v8k93') and text()='Games on Ludio']"))
            )
            return True
        except:
            return False
    
    def click_avatar_user(self):
        avatar_user = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '//img[@alt="avatar" and @src="https://res.cloudinary.com/liars-club/image/upload/c_scale,w_50/v1654378743/ludio_icon_login_fnh2ed.png"]'))
            )
        avatar_user.click()