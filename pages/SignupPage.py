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
        """
        Инициализация страницы регистрации.
        
        :param driver: Экземпляр WebDriver для взаимодействия с браузером.
        """
        url = ConfigProvider().get("ui", "base_url")
        self.__url = url + "sign_up"  # Конструируем URL для страницы регистрации.
        self.__driver = driver

    @allure.step("Перейти на страницу авторизации")
    def go(self):
        """
        Открытие страницы регистрации.
        """
        self.__driver.get(self.__url)

    @allure.step("Ввести email")
    def enter_email(self, email):
        """
        Ввод email в поле регистрации.
        
        :param email: Электронная почта для ввода.
        """
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

    @allure.step("Ввести пароль")
    def enter_password(self, password):
        """
        Ввод пароля в поле.
        
        :param password: Пароль для ввода.
        """
        element = self.__driver.find_element(
            By.XPATH, 
            "//input[@type='password' and @autocomplete='new-password' and contains(@class, 'StyledInput_s1mzwy3')]"
            )
        element.clear()
        element.send_keys(password)

    @allure.step("Подтвердить пароль")
    def confirm_password(self, password):
        """
        Подтверждение пароля в соответствующем поле.
        
        :param password: Подтверждаемый пароль.
        """
        element = self.__driver.find_element(
            By.XPATH, 
            "//input[@type='password' and @autocomplete='off' and contains(@class, 'StyledInput_s1mzwy3')]"
            )
        element.clear()
        element.send_keys(password)

    @allure.step("Нажать на кнопку 'Create account'")
    def click_button_create_account(self):
        """
        Клик по кнопке "Create account".
        """
        WebDriverWait(self.__driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH, 
            "//button[contains(@class, 'StyledButton_s17mzjxz') and @color='#fff' and text()='Create account' and not(@disabled)]"
            ))
    ).click()

    @allure.step("Выбрать тип аккаунта как 'Personal'")
    def account_type_personal(self):
        """
        Выбор типа аккаунта как 'Personal'.
        """
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

    @allure.step("Выбрать тип аккаунта как 'Organization'")
    def account_type_organization(self):
        """
        Выбор типа аккаунта как 'Organization'.
        """
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

    @allure.step("Выбрать имя пользователя")
    def choose_username(self, user_name):
        """
        Ввод имени пользователя.
        
        :param user_name: Имя пользователя.
        """
        element = self.__driver.find_element(
            By.XPATH, 
            '//*[@id="root"]/div[2]/div/div/div/'
            'div/div/div[2]/div[3]/div/div/input'
            )
        element.clear()
        element.send_keys(user_name)

    @allure.step("Отметить чекбокс с политикой конфиденциальности")
    def on_checkbox_privacy_policy(self):
        """
        Отметка чекбокса "Privacy Policy".
        """
        checkbox = self.__driver.find_element(
                By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div/div/div[2]/div[4]/div[1]/div/div/input'
            )
        checkbox.click()

    @allure.step("Отметить чекбокс с правилами сообщества")
    def on_checkbox_community_guidelines(self):
        """
        Отметка чекбокса "Community Guidelines".
        """
        chekbox = self.__driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div[2]/div/div/div/div/div/div[2]/div[5]/div[1]/div/div/input'
        )
        chekbox.click()

    @allure.step("Нажимаем на ссылку 'Terms of Service' и проверяем открытие новой вкладки")
    def click_terms_of_service_and_verify_new_tab(self):
        initial_tabs = self.__driver.window_handles  # Сохраняем список вкладок до клика

        try:
            # Кликаем по ссылке
            terms_link = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'termly.io/document/terms-of-use-for-website') and contains(text(), 'Terms of Service')]"))
            )
            terms_link.click()

            # Ожидаем появления новой вкладки
            WebDriverWait(self.__driver, 10).until(lambda driver: len(driver.window_handles) > len(initial_tabs))

            # Переключаемся на новую вкладку
            new_tabs = self.__driver.window_handles
            new_tab = list(set(new_tabs) - set(initial_tabs))[0]  # Найти ID новой вкладки
            self.__driver.switch_to.window(new_tab)

            # Проверяем, что URL новой вкладки корректный
            expected_url_part = "https://app.termly.io/policy-viewer/policy.html?policyUUID=912ae564-8e3a-4f5f-bc55-7dc9d673a337"
            current_url = self.__driver.current_url
            assert expected_url_part in current_url, f"Ожидали URL содержащий '{expected_url_part}', получили '{current_url}'"

            allure.attach(self.__driver.get_screenshot_as_png(), name="terms_of_service_opened", attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            allure.attach(self.__driver.get_screenshot_as_png(), name="terms_of_service_error", attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Ошибка при открытии 'Terms of Service': {e}")

        finally:
            # Закрываем новую вкладку и возвращаемся к основной
            if len(self.__driver.window_handles) > len(initial_tabs):
                self.__driver.close()
                self.__driver.switch_to.window(initial_tabs[0])
        
    @allure.step("Нажимаем на ссылку 'Privacy Policy' и проверяем открытие новой вкладки")
    def click_privacy_policy_and_verify_new_tab(self):
        initial_tabs = self.__driver.window_handles  # Сохраняем список вкладок до клика

        try:
            # Кликаем по ссылке
            privacy_link = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'termly.io/document/privacy-policy') and contains(text(), 'Privacy Policy')]"))
            )
            privacy_link.click()

            # Ожидаем появления новой вкладки
            WebDriverWait(self.__driver, 10).until(lambda driver: len(driver.window_handles) > len(initial_tabs))

            # Переключаемся на новую вкладку
            new_tabs = self.__driver.window_handles
            new_tab = list(set(new_tabs) - set(initial_tabs))[0]  # Найти ID новой вкладки
            self.__driver.switch_to.window(new_tab)

            # Проверяем, что URL новой вкладки корректный
            expected_url_part = "https://app.termly.io/policy-viewer/policy.html?policyUUID=7365321f-56aa-49b4-9842-3716f44c5c74"
            current_url = self.__driver.current_url
            assert expected_url_part in current_url, f"Ожидали URL содержащий '{expected_url_part}', получили '{current_url}'"

            allure.attach(self.__driver.get_screenshot_as_png(), name="privacy_policy_opened", attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            allure.attach(self.__driver.get_screenshot_as_png(), name="privacy_policy_error", attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Ошибка при открытии 'Privacy Policy': {e}")

        finally:
            # Закрываем новую вкладку и возвращаемся к основной
            if len(self.__driver.window_handles) > len(initial_tabs):
                self.__driver.close()
                self.__driver.switch_to.window(initial_tabs[0])

        
    @allure.step("Нажимаем на ссылку 'Community Guidelines' и проверяем открытие новой вкладки")
    def click_community_guidelines_and_verify_new_tab(self):
        initial_tabs = self.__driver.window_handles  # Сохраняем список вкладок до клика

        # Кликаем по ссылке
        community_link = WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'bit.ly/ludio-community-guidelines') and contains(text(), 'Community Guidelines')]"))
        )
        community_link.click()

        # Ожидаем появления новой вкладки
        WebDriverWait(self.__driver, 10).until(lambda driver: len(driver.window_handles) > len(initial_tabs))

        # Переключаемся на новую вкладку
        new_tabs = self.__driver.window_handles
        new_tab = list(set(new_tabs) - set(initial_tabs))[0]  # Найти ID новой вкладки
        self.__driver.switch_to.window(new_tab)

        # Проверяем, что URL новой вкладки корректный
        expected_url = "https://docs.google.com/document/d/e/2PACX-1vQNJGUG_dgS2HLpjsSytnR2jwk8W1OrUHZ05q2oo1TkKnENniUOaKDrj-kn4aldit6ECpF9YJIFjS5z/pub"
        current_url = self.__driver.current_url
        assert expected_url in current_url, f"Ожидали URL '{expected_url}', получили '{current_url}'"

        allure.attach(self.__driver.get_screenshot_as_png(), name="new_tab_opened", attachment_type=allure.attachment_type.PNG)

        # Закрываем новую вкладку и возвращаемся к основной
        self.__driver.close()
        self.__driver.switch_to.window(initial_tabs[0])

    @allure.step("Проверяем, открылась ли новая вкладка")
    def is_new_tab_opened(self):
        """
        Проверяет, открыта ли новая вкладка в браузере.
        Возвращает True, если количество открытых вкладок больше 1.
        """
        return len(self.__driver.window_handles) > 1

    @allure.step("Нажать кнопку 'Продолжить'")
    def click_button_continue(self):
        """
        Нажимает кнопку 'Continue' на странице, если она доступна.
        """
        self.__driver.find_element(
            By.XPATH,
            "//button[@class='StyledButton_s17mzjxz' and text()='Continue' and not(@disabled)]"
        ).click()

    @allure.step("Нажать кнопку 'Продолжить без аватара'")
    def click_button_continue_without_avatar(self):
        """
        Нажимает кнопку 'Continue without an avatar' на странице.
        """
        button = self.__driver.find_element(
            By.XPATH,
            "//button[text()='Continue without an avatar']"
        )
        button.click()

    @allure.step("Нажать кнопку 'Продолжить' на втором шаге регистрации")
    def click_button_continue_step_2(self):
        """
        Нажимает кнопку 'Continue' на втором шаге регистрации.
        """
        button = self.__driver.find_element(
            By.XPATH,
            '//button[@class="StyledButton_s17mzjxz" and text()="Continue"]'
        )
        button.click()

    @allure.step("Проверяем, отображается ли имя пользователя")
    def is_username_displayed(self, user_name):
        """
        Проверяет, отображается ли имя пользователя на странице.
        :param user_name: Имя пользователя для проверки.
        :return: True, если имя отображается, иначе False.
        """
        try:
            displayed_name = WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    f"//*[contains(text(), '{user_name}')]"
                ))
            )
            return displayed_name.is_displayed()
        except TimeoutException:
            return False

    @allure.step("Добавить аватар")
    def add_avatar_photo(self, file_path):
        """
        Загружает аватар пользователя.
        :param file_path: Путь к файлу аватара.
        """
        button = self.__driver.find_element(
            By.XPATH,
            '//button[@class="StyledButton_s17mzjxz" and text()="Upload an avatar photo"]'
        )
        button.click()

        file_input = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//input[@type="file"]'
            ))
        )
        file_input.send_keys(file_path)

    @allure.step("Проверяем отображение ошибки валидации пароля")
    def error_tooltip_password(self):
        """
        Проверяет, отображается ли сообщение об ошибке валидации пароля.
        :return: True, если ошибка отображается, иначе False.
        """
        try:
            error_tooltip = self.__driver.find_element(
                By.XPATH,
                "//div[contains(@class, 'ErrorHintContainer_')]/div[contains(@class, 'StyledTooltipContainer_')]/div[contains(@class, 'Container_')]"
            )
            return error_tooltip.is_displayed()
        except NoSuchElementException:
            return False

    @allure.step("Проверяем, что заголовок 'Create an account' отображается")
    def is_create_account_header_displayed(self):
        """
        Проверяет, отображается ли заголовок 'Create an account' на странице.
        :return: True, если заголовок отображается, иначе False.
        """
        try:
            return WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'CustomFormHeader_')]/h1[text()='Create an account']"))
            ).is_displayed()
        except Exception:
            return False