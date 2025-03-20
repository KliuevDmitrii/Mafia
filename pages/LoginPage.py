import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from faker import Faker

from configuration.ConfigProvider import ConfigProvider


class LoginPage:
    """
    Этот класс предоставляет методы для выполнения действий на странице авторизации пользователя
    """

    def __init__(self, driver: WebDriver) -> None:
        url = ConfigProvider().get("ui", "base_url")
        self.__url = url+"login"
        self.__driver = driver
        self.fake = Faker()

    @allure.step("Перейти на главную страницу")
    def go(self):
        self.__driver.get(self.__url)

    @allure.step("Перейти на страницу создания нового аккаунта")
    def create_new_accaunt(self):
        self.__driver.find_element(
            By.XPATH,
              "//a[@href='/sign_up']").click()

    @allure.step("Ввести почту в поле email")
    def enter_email(self, email: str):
        element = self.__driver.find_element(By.XPATH, "//input[@type='text' and @autocomplete='new-email' and @class='StyledInput_s1mzwy3']")
        element.clear()
        element.send_keys(email)
        return element.text
    
    @allure.step("Ввести пароль в поле password")
    def enter_password(self, password: str):
        element = self.__driver.find_element(By.XPATH, "//input[@type='password' and @autocomplete='new-password' and contains(@class, 'StyledInput_s1mzwy3')]")
        element.clear()
        element.send_keys(password)

    @allure.step("Нажать кнопку Login")
    def click_button_log_in(self):
        WebDriverWait(self.__driver, 10).until(
        EC.element_to_be_clickable((
            By.XPATH, 
            "//button[contains(@class, 'StyledButton_s17mzjxz') and @color='#fff' and text()='Log in']"))
    ).click()

    @allure.step("Кнопка Login не активна")    
    def find_disabled_login_button(self):
        try:
            button = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, 
                '//button[@class="StyledButton_s17mzjxz" and @disabled and text()="Log in"]'))
        )
            return button.get_attribute("disabled") is not None
        except TimeoutException:
            return False
    
    @allure.step("Нажать кнопку New call")
    def click_new_call_button(self):
        try:
            button = WebDriverWait(self.__driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, 
                "//button[@color='#fff' and contains(@class, 'StyledButton_s17mzjxz') and not(@disabled)]"))
        )
            button.click()
            return True
        except TimeoutException:
            print("Активная кнопка не найдена")
            return False

    @allure.step("Формат почты не валидный")    
    def invalid_email_format(self) -> str:
        error = self.__driver.find_element(By.XPATH, '//label[@class="ErrorLabel_e1h592ms" and contains(text(), "Invalid Email Format")]')
        return error.text
    
    @allure.step("Нажать кнопку Log out")
    def click_button_log_out(self):
        button = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, 
                "//button[@class='StyledButton_s17mzjxz' and @color='#ccc']"))
        )
        button.click()

    def generate_invalid_email(self):
        invalid_email_samples = [
            self.fake.user_name(),
            self.fake.domain_name(),
            self.fake.user_name() + "@@",
            self.fake.user_name() + "@com",
            " " + self.fake.email(),
            self.fake.email() + " ",
            self.fake.email().replace("@", " ")
        ]
        return self.fake.random.choice(invalid_email_samples)
        