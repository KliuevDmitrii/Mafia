import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from configuration.ConfigProvider import ConfigProvider

class ProfilePage:
    """
    Этот класс предоставляет методы для выполнения действий на странице профиля пользователя
    """

    def __init__(self, driver: WebDriver) -> None:
        url = ConfigProvider().get("ui", "base_url")
        self.__url = url+"profile"
        self.__driver = driver

    @allure.step("Перейти на главную страницу")
    def go(self):
        self.__driver.get(self.__url)

    @allure.step("Нажать кнопку Edit")
    def click_button_edit(self):
        edit_button = WebDriverWait(self.__driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH, 
                '//button[@color="#55AA64" and @class="StyledButton_s17mzjxz" and text()="Edit"]'
            ))
        )
        edit_button.click()

    @allure.step("Ввести в поле Name новое имя")
    def input_name(self, new_name: str) -> str:
        input_field = WebDriverWait(self.__driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH,
                f'//*[@id="root"]/div/div/div[2]/div/div[2]/div/div[1]/div[3]/div[1]/div/div/input'
                ))
            )
        time.sleep(5)
        input_field.clear()
        time.sleep(5)
        input_field.send_keys(new_name)
        time.sleep(5)
        return input_field.get_attribute("value")
    
    @allure.step("Нажать кнопку Save")
    def click_button_save(self):
        time.sleep(5)
        save_button = WebDriverWait(self.__driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH, 
                '//button[@class="StyledButton_s17mzjxz" and text()="Save"]'
            ))
        )
        save_button.click()
        time.sleep(5)

    @allure.step("Ввести в поле pronouns новое значение")
    def input_pronouns(self, pronouns: str) -> str:
        input_field = WebDriverWait(self.__driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH,
                f'//*[@id="root"]/div/div/div[2]/div/div[2]/div/div[1]/div[3]/div[2]/div/div/input'
            ))
        )
        input_field.clear()
        input_field.send_keys(pronouns)
        return input_field.get_attribute("value")
    
    @allure.step("Проверка нового значения в Pronouns")
    def check_user_pronouns(self):
        try:
            time.sleep(5)
            pronouns_element = WebDriverWait(self.__driver, 40).until(
            EC.presence_of_element_located((
                By.XPATH,
                f'//*[@id="root"]/div[2]/div/div[2]/div/div[2]/div/div[1]/div[3]/div[2]/div'
            ))
        )
            pronouns_text = pronouns_element.text
            return pronouns_text
        except TimeoutException:
            return None

    @allure.step("Проверить имя пользователя")
    def check_user_name(self):
        try:
            time.sleep(5)
            name_element = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//div[@class="UsernameEmailCustom_u14t02mx"]/h6'
            ))
        )
            name_text = name_element.text
            return name_text
        except TimeoutException:
            return None

    @allure.step("Проверить почту пользователя")
    def check_user_email(self):
        try:
            email_element = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//div[@class="UsernameEmailCustom_u14t02mx"]/p'
            ))
        )
            email_text = email_element.text
            return email_text
        except TimeoutException:
            return None
        
    # Billing information
    
    @allure.step("Нажать на вкладку Billing information")
    def click_tab_billing_information(self):
        billing_info_tab = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//div[@class="CustomNavbarItem_cvzvmhi" and text()="Billing information"]'
            ))
        )
        billing_info_tab.click()

    @allure.step("Нажать кнопку Update")
    def click_button_update(self):
        time.sleep(3)
        update_button = WebDriverWait(self.__driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//button[@class='StyledButton_s17mzjxz' and text()='Update']"
            ))
        )
        update_button.click()

    @allure.step("Выбоать план подптски на месяц")
    def subscription_plan_monthly(self):
        time.sleep(2)
        monthly = WebDriverWait(self.__driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH, 
                '//div[contains(@class, "PlanCardDefault_plevllw") and .//h3[text()="Monthly"]]'
            ))
        )
        monthly.click()

    @allure.step("Выбрать план подписки на год")
    def subscription_plan_annual(self):
        time.sleep(2)
        annual = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, 
                '//div[contains(@class, "PlanCardDefault_plevllw") and .//h3[text()="Annual"]]'
            ))
        )
        annual.click()
    
    @allure.step("Нажать кнопку Continue")
    def click_button_continue(self):
        continue_button = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//button[@class='ContinueButton_cpp8ujb StyledButton_s17mzjxz' and text()='Continue']"
            ))
        )
        continue_button.click()

    @allure.step("Ввести: номер карты, срок действия карты, CVC карты, имя держателя карты")
    def add_card(self, card_number: int, card_date: int, card_cvc: int, cardholder_name: str):
        time.sleep(4)
        iframe = WebDriverWait(self.__driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='elements-inner-card']"))
        )
        self.__driver.switch_to.frame(iframe)

        number_input =  WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//input[@name="cardnumber" and @autocomplete="cc-number" and @type="text" and @inputmode="numeric"]'
            ))
        )
        number_input.clear()
        number_input.send_keys(card_number)

        date_field = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//input[@placeholder="ММ / ГГ"]'
            ))
        )
        date_field.clear()
        date_field.send_keys(card_date)

        cvc_field = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//input[@name='cvc']"
            ))
        )
        cvc_field.clear()
        cvc_field.send_keys(card_cvc)

        cardholder_field = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//input[@placeholder='Cardholder name']"
            ))
        )
        cardholder_field.clear()
        cardholder_field.send_keys(cardholder_name)

        self.__driver.switch_to.default_content()

    @allure.step("Нажать кнопку Start my subscription")
    def click_button_start_my_subscription(self):
        start_my_subscription_button = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//button[text()='Start my subscription!']"
            ))
        )
        start_my_subscription_button.click()

    @allure.step("Нажать кнопку Confirm")
    def click_button_confirm(self):
        confirm_button = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//button[text()='Confirm']"
            ))
        )
        confirm_button.click()

    @allure.step("Нажать кнопку Cancel")
    def click_button_cancel(self):
        cancel_button = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//button[text()='Cancel']"
            ))
        )
        cancel_button.click()
        
    @allure.step("Закрыть окно добавления метода оплаты")
    def close_popup_payment_settings(self):
        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//div[contains(@style, 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3Zn')]"
            ))
        ).click()

    @allure.step("Проверка добавления новой карты")
    def check_new_card_add(self):
        card_number = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//div[contains(@class, 'CardName_c1un9bd') and contains(text(), '...')]"
            ))
        )
        displayed_card_number = card_number.text


    @allure.step("Проверка оставшихся Remaining passes")
    def check_remaining_passes(self):
        try:
            remaining_passes = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '//div[@class="Container_cpo1j0r" and .//div[@class="NameCustom_n11c1htd" and text()="Remaining passes"]]//div[@class="ValueCustom_v182qmkw"]'
            ))
        )
            return remaining_passes.text
        except TimeoutException:
            print("Элемент не найден")
            return None