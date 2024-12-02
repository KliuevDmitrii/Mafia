from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPage:
    def __init__(self, driver):
        self._driver = driver

    def get(self):
        self._driver.get("https://dev.ludio.gg/login")

    def enter_email(self, email):
        element = self._driver.find_element(By.XPATH, "//input[@type='text' and @autocomplete='new-email' and @class='StyledInput_s1mzwy3']")
        element.clear()
        element.send_keys(email)

    def enter_password(self, password):
        element = self._driver.find_element(By.XPATH, "//input[@type='password' and @autocomplete='new-password' and contains(@class, 'StyledInput_s1mzwy3')]")
        element.clear()
        element.send_keys(password)

    def click_button_log_in(self):
        WebDriverWait(self._driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'StyledButton_s17mzjxz') and @color='#fff' and text()='Log in']"))
    ).click()

    def click_new_call_button(self):
        try:
        # Ожидание до 10 секунд появления активной кнопки с заданным цветом и классом
            button = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, 
                "//button[@color='#fff' and contains(@class, 'StyledButton_s17mzjxz') and not(@disabled)]"))
        )
            button.click()
            return True
        except TimeoutException:
            print("Активная кнопка не найдена")
            return False