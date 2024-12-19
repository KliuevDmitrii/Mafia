import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys



class ProfilePage:
    def __init__(self, driver):
        self._driver = driver

    def get(self):
        self._driver.get("https://dev.ludio.gg/profile")

    def click_button_edit(self):
        edit_button = WebDriverWait(self._driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH, 
                '//button[@color="#55AA64" and @class="StyledButton_s17mzjxz" and text()="Edit"]'
            ))
        )
        edit_button.click()

    def input_name(self, new_name):
        input_field = WebDriverWait(self._driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//input[@type="text" and @class="StyledInput_s1mzwy3"]'))
            )
        input_field.clear()
        input_field.send_keys(new_name)
        return input_field.get_attribute("value")
    
    def click_button_save(self):
        save_button = WebDriverWait(self._driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH, 
                '//button[@class="StyledButton_s17mzjxz" and text()="Save"]'
            ))
        )
        save_button.click()

    def input_pronouns(self, pronouns):
        input_field = WebDriverWait(self._driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH,
                f'//*[@id="root"]/div/div/div[2]/div/div[2]/div/div[1]/div[3]/div[2]/div/div/input'
            ))
        )
        input_field.clear()
        input_field.send_keys(pronouns)
        return input_field.get_attribute("value")
    
    def check_user_pronouns(self):
        try:
            time.sleep(5)
            pronouns_element = WebDriverWait(self._driver, 40).until(
            EC.presence_of_element_located((
                By.XPATH,
                f'//*[@id="root"]/div[2]/div/div[2]/div/div[2]/div/div[1]/div[3]/div[2]/div'
            ))
        )
            pronouns_text = pronouns_element.text
            return pronouns_text
        except TimeoutException:
            return None

    def check_user_name(self):
        try:
            name_element = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//div[@class="UsernameEmailCustom_u14t02mx"]/h6'
            ))
        )
            name_text = name_element.text
            return name_text
        except TimeoutException:
            return None

    def check_user_email(self):
        try:
            email_element = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//div[@class="UsernameEmailCustom_u14t02mx"]/p'
            ))
        )
            email_text = email_element.text
            return email_text
        except TimeoutException:
            return None

    def click_tab_billing_information(self):
        billing_info_tab = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//div[@class="CustomNavbarItem_cvzvmhi" and text()="Billing information"]'
            ))
        )
        billing_info_tab.click()

    def check_remaining_passes(self):
        try:
            remaining_passes = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '//div[@class="Container_cpo1j0r" and .//div[@class="NameCustom_n11c1htd" and text()="Remaining passes"]]//div[@class="ValueCustom_v182qmkw"]'
            ))
        )
            return remaining_passes.text
        except TimeoutException:
            print("Элемент не найден")
            return None