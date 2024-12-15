from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class ProfilePage:
    def __init__(self, driver):
        self._driver = driver

    def get(self):
        self._driver.get("https://dev.ludio.gg/profile")

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