import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from configuration.ConfigProvider import ConfigProvider

class ResetPasswordPage:

    def __init__(self, driver: WebDriver) -> None:
        url = ConfigProvider().get("ui", "base_url")
        self.__url = url+"login"
        self.__driver = driver


    @allure.step("Перейти на страницу авторизации")
    def go(self):
        self.__driver.get(self.__url)

    def forgot_password(self):
        self.__driver.find_element(
            By.XPATH,
              "//a[@href='/reset_password' and text()='Forgot password?']").click()
        
    def enter_email(self, email):
        try:
            email_field = WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@class='InputContainer_i1fs9mej']//input[@type='text' and @class='StyledInput_s1mzwy3']")
                )
            )
            email_field.clear()
            email_field.send_keys(email)

        except TimeoutException:
            print("Поле для ввода email не доступно.")
            raise


    def click_button_reset_password(self):
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((
            By.XPATH, 
            "//button[@class='StyledButton_s17mzjxz' and normalize-space(text())='Reset password']"
            ))
    ).click()
        
    def button_reset_password_disabled(self):
        try:
            button = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((
                By.XPATH, 
                "//button[@class='StyledButton_s17mzjxz' and normalize-space(text())='Reset password']"
            ))
        )
            return button.get_attribute("disabled") is not None
        except TimeoutException:
            print("Кнопка сброса пароля не найдена.")
            return False
        
    def popup(self):
        try:
            popup = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//p[normalize-space(text())='We have sent you instructions to change your password by email.']"
                ))
            )
            return popup.text
        except TimeoutException:
            return None
        
    def popup_alert(self):
        try:
            popup = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//div[@role='alert']"
                ))
            )
            return popup
        except TimeoutException:
            return None