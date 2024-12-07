from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class SignupPage:
    def __init__(self, driver):
        self._driver = driver

    def get(self):
        self._driver.get("https://dev.ludio.gg/login")

    def create_new_accaunt(self):
        self._driver.find_element(By.XPATH, "//a[@href='/sign_up']").click()

    def enter_email(self, email):
        try:
            element = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, 
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
        element = self._driver.find_element(By.XPATH, 
                                            "//input[@type='password' and @autocomplete='new-password' and contains(@class, 'StyledInput_s1mzwy3')]")
        element.clear()
        element.send_keys(password)

    def confirm_password(self, password):
        element = self._driver.find_element(By.XPATH, 
                                            "//input[@type='password' and @autocomplete='off' and contains(@class, 'StyledInput_s1mzwy3')]")
        element.clear()
        element.send_keys(password)

    def click_button_create_account(self):
        WebDriverWait(self._driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, 
                                    "//button[contains(@class, 'StyledButton_s17mzjxz') and @color='#fff' and text()='Create account' and not(@disabled)]"))
    ).click()
        
    def account_tipe_personal(self):
        self._driver.find_element(By.XPATH, "//div[@class='RightIconContainer_r155e2tn' and contains(@style, '--r155e2tn-0: pointer;')]").click()
        element = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='DropdownContent_d1prohsz' and text()='Personal']"))
        )
        element.click()

    def account_tipe_organization(self):
        self._driver.find_element(By.XPATH, "//div[@class='RightIconContainer_r155e2tn' and contains(@style, '--r155e2tn-0: pointer;')]").click()
        element = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='DropdownContent_d1prohsz' and text()='Organization']"))
        )
        element.click()

    def choose_username(self, user_name):
            element = self._driver.find_element(By.XPATH, 
                                                '//*[@id="root"]/div[2]/div/div/div/'
                                                'div/div/div[2]/div[3]/div/div/input'
                                                )
            element.clear()
            element.send_keys(user_name)

    def on_checkbox_privacy_policy(self):
        try:
            checkbox = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, 
                                            "//*[@id='root']/div[2]/div/div/div/div/div/div[2]/div[4]/div[1]/div/div/input"))
        )
            checkbox.click()
        except TimeoutException:
            print("Чекбокс не стал доступен для клика в течение 10 секунд.")
            raise

    def on_checkbox_community_guidelines(self):
        chekbox = self._driver.find_element(By.XPATH,
                                             "//*[@id='root']/div[2]/div/div/div/div/div/div[2]/div[5]/div[1]/div/div/input")
        chekbox.click()

    def click_button_continue(self):
        self._driver.find_element(By.XPATH, "//button[@class='StyledButton_s17mzjxz' and text()='Continue' and not(@disabled)]").click()

    def click_button_continue_without_avatar(self):
        try:
            button = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='StyledButton_s17mzjxz' and text()='Continue' and not(@disabled)]"))
            )
            button.click()
        except TimeoutException:
            print("Кнопка 'Continue' не доступна для клика.")
            raise

    def verify_username_displayed(self, user_name):
        try:
            displayed_name = WebDriverWait(self._driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{user_name}')]"))
            )
            assert displayed_name.is_displayed(), f"Имя пользователя '{user_name}' не отображается на странице."
        except TimeoutException:
            raise AssertionError(f"Имя пользователя '{user_name}' не найдено.")
    