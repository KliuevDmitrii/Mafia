import allure
import time

from faker import Faker
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from configuration.ConfigProvider import ConfigProvider

fake = Faker()

class SignupPage:
    
    def __init__(self, driver: WebDriver) -> None:
        url = ConfigProvider().get("ui", "base_url")
        self.__url = url+"sign_up"
        self.__driver = driver

    @allure.step("Перейти на страницу авторизации")
    def go(self):
        self.__driver.get(self.__url)

    def enter_email(self, email):
        try:
            element = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH, 
                    "//div[@class='InputContainer_i1fs9mej']"
                    "//label[contains(text(),'Email')]"
                    "/following-sibling::input"))
            )
            element.clear()
            element.send_keys(email)
        except TimeoutException:
            print("Поле для ввода email не доступно.")
            raise

    def enter_password(self, password):
        element = self.__driver.find_element(
            By.XPATH, 
            "//input[@type='password' and @autocomplete='new-password' and contains(@class, 'StyledInput_s1mzwy3')]"
            )
        element.clear()
        element.send_keys(password)

    def confirm_password(self, password):
        element = self.__driver.find_element(
            By.XPATH, 
            "//input[@type='password' and @autocomplete='off' and contains(@class, 'StyledInput_s1mzwy3')]"
            )
        element.clear()
        element.send_keys(password)

    def click_button_create_account(self):
        WebDriverWait(self.__driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH, 
            "//button[contains(@class, 'StyledButton_s17mzjxz') and @color='#fff' and text()='Create account' and not(@disabled)]"
            ))
    ).click()
        
    def account_type_personal(self):
        self.__driver.find_element(
            By.XPATH,
            '//div[@cursor="pointer" and contains(@class, "RightIconContainer_r155e2tn")]'
            ).click()
        element = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH, 
                    '//div[@class="DropdownContent_d1prohsz" and text()="Personal"]'))
        )
        element.click()

    def account_type_organization(self):
        self.__driver.find_element(
            By.XPATH,
            '//div[@cursor="pointer" and contains(@class, "RightIconContainer_r155e2tn")]'
            ).click()
        element = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH, 
                    '//*[@id="root"]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/ul/li[1]'))
        )
        element.click()

    def choose_username(self, user_name):
            element = self.__driver.find_element(
                By.XPATH, 
                '//*[@id="root"]/div[2]/div/div/div/'
                'div/div/div[2]/div[3]/div/div/input'
                )
            element.clear()
            element.send_keys(user_name)

    def on_checkbox_privacy_policy(self):
        checkbox = self.__driver.find_element(
                By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div/div/div[2]/div[4]/div[1]/div/div/input'
            )
        checkbox.click()

    def on_checkbox_community_guidelines(self):
        chekbox = self.__driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div[2]/div/div/div/div/div/div[2]/div[5]/div[1]/div/div/input'
        )
        chekbox.click()

    def click_button_continue(self):
        self.__driver.find_element(
            By.XPATH,
            "//button[@class='StyledButton_s17mzjxz' and text()='Continue' and not(@disabled)]"
            ).click()

    def click_button_continue_without_avatar(self):
        button = self.__driver.find_element(
                    By.XPATH,
                    "//button[text()='Continue without an avatar']")
        button.click()
    
    def click_button_continue_step_2(self):
        button = self.__driver.find_element(
                    By.XPATH,
                    '//button[@class="StyledButton_s17mzjxz" and text()="Continue"]')
        button.click()

    def is_username_displayed(self, user_name):
        try:
            displayed_name = WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                f"//*[contains(text(), '{user_name}')]"))
        )
            return displayed_name.is_displayed()
        except TimeoutException:
           return False

    def add_avatar_photo(self, file_path):
        button = self.__driver.find_element(
        By.XPATH,
        '//button[@class="StyledButton_s17mzjxz" and text()="Upload an avatar photo"]'
        )
        button.click()
        
        file_input = WebDriverWait(self.__driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH,
            '//input[@type="file"]'))
        )
        file_input.send_keys(file_path)

    def error_tooltip_password(self):
        try:
            error_tooltip = self.__driver.find_element(
            By.XPATH, "//div[contains(@class, 'ErrorHintContainer_')]/div[contains(@class, 'StyledTooltipContainer_')]/div[contains(@class, 'Container_')]"
            )
            return error_tooltip.is_displayed()
        except NoSuchElementException:
            return False