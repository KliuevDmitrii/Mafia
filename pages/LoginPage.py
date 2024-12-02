from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self._driver = driver
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
        self._driver.find_element(By.XPATH, "//button[@disabled='' and contains(@class, 'StyledButton_s17mzjxz') and @color='#fff' and text()='Log in']").click()
