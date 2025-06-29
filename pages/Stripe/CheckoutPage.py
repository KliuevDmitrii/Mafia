import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
import re
from faker import Faker

from configuration.ConfigProvider import ConfigProvider

fake = Faker()

class CheckoutPage:
    """
    Этот класс предоставляет методы для выполнения действий на странице оплаты Stripe.
    """
     
    def __init__(self, driver: WebDriver) -> None:
        """
        Получение базового URL из конфигурации
        """
        url = ConfigProvider().get("ui", "pay_url")
        self.__url = url
        self.__driver = driver

    @allure.step("Перейти на страницу оплаты")
    def go(self):
        """
        Переход на страницу оплаты
        """
        self.__driver.get(self.__url)

    @allure.step("Получить текущий URL страницы оплаты")
    def get_current_url(self) -> str:
        """
        Получение текущего URL страницы оплаты
        """
        return self.__driver.current_url
    
    @allure.step("Проверить, что страница оплаты загружена")
    def is_page_loaded(self):
        try:
            WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//h1[contains(text(), 'Checkout')]"))
            )
            return True
        except TimeoutException:
            return False
        
    @allure.step("Получить email пользователя из формы Stripe Checkout")
    def get_user_email(self) -> str:
        """
        Возвращает email, отображаемый на форме оплаты Stripe.
        """
        try:
            email_element = WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//div[contains(@class, 'ReadOnlyFormField-title') and contains(text(), '@')]"
                ))
            )
            email_text = email_element.text.strip()
            allure.attach(email_text, name="Email на форме Stripe", attachment_type=allure.attachment_type.TEXT)
            return email_text
        except TimeoutException:
            raise Exception("Email не найден на странице Stripe Checkout.")


    @allure.step("Выбрать метод оплаты 'Карта'")
    def select_payment_method_card(self):
        """
        Находит и нажимает кнопку 'Оплатить картой'
        """
        time.sleep(5)
        try:
            card_option = WebDriverWait(self.__driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='card-accordion-item-button']"))
            )
            card_option.click()
        except TimeoutException:
            raise Exception("Кнопка 'Оплатить картой' не найдена.")

        
    @allure.step("Ввести данные карты")
    def enter_card_details(self, card_number: str, expiry_date: str, cvc: str, placeholder: str):
        """
        Ввод данных карты в соответствующие поля
        """
        card_number_field = self.__driver.find_element(By.XPATH, "//input[@id='cardNumber']")
        expiry_date_field = self.__driver.find_element(By.XPATH, "//input[@id='cardExpiry']")
        cvc_field = self.__driver.find_element(By.XPATH, "//input[@id='cardCvc']")
        placeholder_field = self.__driver.find_element(By.XPATH, "//input[@id='billingName']")

        card_number_field.clear()
        card_number_field.send_keys(card_number)
        
        expiry_date_field.clear()
        expiry_date_field.send_keys(expiry_date)
        
        cvc_field.clear()
        cvc_field.send_keys(cvc)

        placeholder_field.clear()
        placeholder_field.send_keys(placeholder)

    @allure.step("Нажать кнопку 'Подписаться'")
    def click_submit_button(self):
        """
        Нажимает кнопку 'Подписаться' на странице Stripe Checkout.
        """
        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[.//div[contains(@class, 'SubmitButton-IconContainer')]]"))
        ).click()

    @allure.step("Получить сумму подписки из Stripe Checkout")
    def get_subscription_amount(self) -> float:
        """
        Извлекает сумму подписки на странице Stripe Checkout и возвращает её как float.
        """
        try:
            amount_element = WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//span[contains(@class, 'CurrencyAmount')]"
                ))
            )
            amount_text = amount_element.text.strip()
            allure.attach(amount_text, name="Текст с суммой", attachment_type=allure.attachment_type.TEXT)

            normalized_amount = amount_text.replace('\xa0', '').replace(',', '.').replace('$', '').strip()

            match = re.search(r"(\d{1,3}(?:\.\d{1,2})?)", normalized_amount)
            if not match:
                raise ValueError(f"Не удалось извлечь сумму из текста: '{amount_text}'")

            amount = float(match.group(1))
            allure.attach(str(amount), name="Извлечённая сумма", attachment_type=allure.attachment_type.TEXT)

            return amount
        except TimeoutException:
            raise TimeoutException("Сумма подписки на Stripe Checkout не найдена за отведённое время.")

