import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from configuration.ConfigProvider import ConfigProvider

from faker import Faker

fake = Faker()

class ProfilePage:
    """
    Этот класс предоставляет методы для выполнения действий на странице профиля пользователя.
    Все действия описаны через шаги Allure для лучшего логирования.
    """

    def __init__(self, driver: WebDriver) -> None:
        # Получение базового URL из конфигурации и добавление "/profile" для формирования URL страницы профиля
        url = ConfigProvider().get("ui", "base_url")
        self.__url = url+"profile"
        self.__driver = driver

    @allure.step("Перейти на главную страницу")
    def go(self):
        """Открывает страницу профиля пользователя."""
        self.__driver.get(self.__url)

    @allure.step("Нажать кнопку Edit")
    def click_button_edit(self):
        """Нажимает кнопку "Edit" для редактирования профиля."""
        edit_button = WebDriverWait(self.__driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH, 
                '//button[@color="#55AA64" and @class="StyledButton_s17mzjxz" and text()="Edit"]'
            ))
        )
        edit_button.click()

    @allure.step("Ввести в поле Name новое имя")
    def input_name(self, new_name: str) -> str:
        """Вводит новое имя в поле 'Name'."""
        input_field = WebDriverWait(self.__driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//p[contains(@class, 'DescriptionTextCustom_d16oteua')][contains(text(), 'Username')]/following-sibling::div//input"
                ))
            )
        time.sleep(5)  # Не рекомендуется использовать time.sleep, лучше использовать ожидания
        input_field.clear()  # Очищает поле ввода
        time.sleep(5)
        input_field.send_keys(new_name)  # Вводит новое имя
        time.sleep(5)
        return input_field.get_attribute("value")  # Возвращает введенное значение

    @allure.step("Нажать кнопку Save")
    def click_button_save(self):
        """Нажимает кнопку "Save" для сохранения изменений."""
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
        """Вводит новое значение в поле 'Pronouns'."""
        input_field = WebDriverWait(self.__driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//p[contains(@class, 'DescriptionTextCustom_d16oteua')][contains(text(), 'Pronouns')]/following-sibling::div//input"
            ))
        )
        input_field.clear()  # Очищает поле ввода
        time.sleep(5)
        input_field.send_keys(pronouns)  # Вводит значение местоимений
        return input_field.get_attribute("value")  # Возвращает введенное значение

    @allure.step("Проверка нового значения в Pronouns")
    def check_user_pronouns(self):
        """Проверяет отображаемое значение местоимений."""
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
            return None  # Возвращает None, если элемент не был найден

    @allure.step("Проверить имя пользователя")
    def check_user_name(self):
        """Проверяет отображаемое имя пользователя."""
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
        """Проверяет отображаемый адрес электронной почты пользователя."""
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
        
    # Раздел для работы с информацией о платеже

    @allure.step("Нажать на вкладку Billing information")
    def click_tab_billing_information(self):
        """Нажимает на вкладку 'Billing information'."""
        billing_info_tab = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//div[@class="CustomNavbarItem_cvzvmhi" and text()="Billing information"]'
            ))
        )
        billing_info_tab.click()

    @allure.step("Нажать кнопку Update")
    def click_button_update(self):
        """Нажимает кнопку 'Update' для обновления информации о платеже."""
        time.sleep(3)
        update_button = WebDriverWait(self.__driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//button[@class='StyledButton_s17mzjxz' and text()='Update']"
            ))
        )
        update_button.click()

    @allure.step("Выбоать план подписки на месяц")
    def subscription_plan_monthly(self):
        """Выбирает план подписки на месяц."""
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
        """Выбирает план подписки на год."""
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
        """Нажимает кнопку 'Continue'."""
        continue_button = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//button[@class='ContinueButton_cpp8ujb StyledButton_s17mzjxz' and text()='Continue']"
            ))
        )
        continue_button.click()

    @allure.step("Ввести: номер карты, срок действия карты, CVC карты, имя держателя карты")
    def add_card(self, card_number: int, card_date: int, card_cvc: int, cardholder_name: str):
        """Добавляет информацию о карте (номер, срок действия, CVC и имя владельца)."""
        time.sleep(4)
        iframe = WebDriverWait(self.__driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='elements-inner-card']"))
        )
        self.__driver.switch_to.frame(iframe)

        # Ввод данных карты
        number_input =  WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//input[@name="cardnumber" and @autocomplete="cc-number" and @type="text" and @inputmode="numeric"]'
            ))
        )
        number_input.clear()
        number_input.send_keys(card_number)

        # Ввод срока действия карты
        date_field = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//input[@placeholder="ММ / ГГ"]'
            ))
        )
        date_field.clear()
        date_field.send_keys(card_date)

        # Ввод CVC
        cvc_field = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//input[@name='cvc']"
            ))
        )
        cvc_field.clear()
        cvc_field.send_keys(card_cvc)

        # Ввод имени держателя карты
        cardholder_field = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//input[@placeholder='Cardholder name']"
            ))
        )
        cardholder_field.clear()
        cardholder_field.send_keys(cardholder_name)

        self.__driver.switch_to.default_content()  # Возвращаемся к основной странице

    # @allure.step("Ввести: имя держателя карты")
    # def add_cardholder_name(self, cardholder_name: str):
    #     """Добавляет информацию о карте (имя владельца)."""
    #     time.sleep(4)
    #     cardholder_field = WebDriverWait(self.__driver, 10).until(
    #         EC.presence_of_element_located((
    #             By.XPATH,
    #             "//input[@placeholder='Cardholder name']"
    #         ))
    #     )
    #     cardholder_field.clear()
    #     cardholder_field.send_keys(cardholder_name)

    @allure.step("Нажать кнопку Start my subscription")
    def click_button_start_my_subscription(self):
        """Нажимает кнопку 'Start my subscription!'."""
        start_my_subscription_button = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//button[text()='Start my subscription!']"
            ))
        )
        start_my_subscription_button.click()

    @allure.step("Нажать кнопку Confirm")
    def click_button_confirm(self):
        """Нажимает кнопку 'Confirm'."""
        confirm_button = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//button[text()='Confirm']"
            ))
        )
        confirm_button.click()

    @allure.step("Нажать кнопку Cancel")
    def click_button_cancel(self):
        """Нажимает кнопку 'Cancel'."""
        cancel_button = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//button[text()='Cancel']"
            ))
        )
        cancel_button.click()
        
    @allure.step("Закрыть окно добавления метода оплаты")
    def close_popup_payment_settings(self):
        """Закрывает окно добавления метода оплаты."""
        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//div[contains(@style, 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3Zn')]"
            ))
        ).click()

    @allure.step("Проверка добавления новой карты")
    def check_new_card_add(self):
        """Проверяет добавление новой карты."""
        card_number = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//div[contains(@class, 'CardName_c1un9bd') and contains(text(), '...')]"
            ))
        )
        displayed_card_number = card_number.text


    @allure.step("Проверка оставшихся Remaining passes")
    def check_remaining_passes(self):
        """Проверяет количество оставшихся пропусков (Remaining passes)."""
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
            return None  # Возвращает None, если элемент не был найден
