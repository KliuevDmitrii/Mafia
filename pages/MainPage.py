from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainPage:
    def __init__(self, driver):
        self._driver = driver

    def get(self):
        self._driver.get("https://dev.ludio.gg/")

    def is_page_loaded(self):
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'GamesTitle_g6v8k93') and text()='Games on Ludio']"))
            )
            return True
        except:
            return False
    