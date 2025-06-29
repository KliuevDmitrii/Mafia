import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from configuration.ConfigProvider import ConfigProvider

class MainPage:
    """
    Этот класс предоставляет методы для выполнения действий на странице пользователя.
    """
     
    def __init__(self, driver: WebDriver) -> None:
        """
        Получение базового URL из конфигурации
        """
        url = ConfigProvider().get("ui", "base_url")
        self.__url = url
        self.__driver = driver

    @allure.step("Перейти на главную страницу")
    def go(self):
        """ 
        Переход на главную страницу пользователя 
        """
        self.__driver.get(self.__url)

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        """
        Получение текущего URL страницы
        """
        return self.__driver.current_url

    @allure.step("Страница пользователя открыта")
    def is_page_loaded(self):
        """ Проверяет, что страница пользователя загружена.
        """
        try:
            # Ожидание появления заголовка "Games on Ludio" на странице
            WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//h2[contains(@class, 'GamesTitle_g6v8k93') and text()='Games on Ludio']"))
            )
            return True
        except:
            return False
    
    @allure.step("Нажать на аватар пользователя")
    def click_avatar_user(self):
        '''
        Нажимает на аватар пользователя для перехода на страницу профиля.
        '''
        time.sleep(3)
        avatar_user = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '//div[@class="ProfileLinkWrapper_p2ot533"]//img[@alt="avatar"]'))
            )
        # Клик по аватару пользователя
        avatar_user.click()

    def is_div_element_name_user(self):
        """
        Проверяет, существует ли элемент div, содержащий изображение SVG.
        """
        try:
            self.__driver.find_element(By.XPATH, '//div[@width="100%" and @height="100%" and contains(@src, "data:image/svg+xml")]')
            return True
        except NoSuchElementException:
            return False
        
    @allure.step("Кликнуть по кнопке 'Discord' и проверить открытие новой вкладки")
    def click_discord_button(self):
        """
        Кликает по кнопке Discord и проверяет открытие новой вкладки с Discord.
        """
        config = ConfigProvider()
        expected_url_part = config.get_social_link("discord_url")

        initial_tabs = self.__driver.window_handles

        try:
            discord_button = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//span[contains(@class, 'CustomMenuSocialLinksTitle') and text()='Discord']"
                ))
            )
            discord_button.click()

            WebDriverWait(self.__driver, 10).until(lambda driver: len(driver.window_handles) > len(initial_tabs))

            new_tabs = self.__driver.window_handles
            new_tab = list(set(new_tabs) - set(initial_tabs))[0]
            self.__driver.switch_to.window(new_tab)

            current_url = self.__driver.current_url
            assert expected_url_part in current_url, f"Ожидали URL содержащий '{expected_url_part}', получили '{current_url}'"

            allure.attach(self.__driver.get_screenshot_as_png(), name="discord_tab_opened", attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            allure.attach(self.__driver.get_screenshot_as_png(), name="discord_tab_error", attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Ошибка при открытии ссылки Discord: {e}")

        finally:
            if len(self.__driver.window_handles) > len(initial_tabs):
                self.__driver.close()
                self.__driver.switch_to.window(initial_tabs[0])

        
    @allure.step("Кликнуть по кнопке 'Instagram' и проверить открытие новой вкладки")
    def click_instagram_button(self):
        """
        Кликает по кнопке Instagram и проверяет открытие новой вкладки.
        """
        from configuration.ConfigProvider import ConfigProvider
        config = ConfigProvider()
        expected_url_part = config.get_social_link("instagram_url")

        initial_tabs = self.__driver.window_handles

        try:
            instagram_button = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//span[contains(@class, 'CustomMenuSocialLinksTitle') and text()='Instagram']"
                ))
            )
            instagram_button.click()

            WebDriverWait(self.__driver, 10).until(lambda driver: len(driver.window_handles) > len(initial_tabs))

            new_tabs = self.__driver.window_handles
            new_tab = list(set(new_tabs) - set(initial_tabs))[0]
            self.__driver.switch_to.window(new_tab)

            current_url = self.__driver.current_url
            assert expected_url_part in current_url, f"Ожидали URL '{expected_url_part}', получили '{current_url}'"

            allure.attach(self.__driver.get_screenshot_as_png(), name="instagram_tab_opened", attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            allure.attach(self.__driver.get_screenshot_as_png(), name="instagram_tab_error", attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Ошибка при открытии Instagram: {e}")

        finally:
            if len(self.__driver.window_handles) > len(initial_tabs):
                self.__driver.close()
                self.__driver.switch_to.window(initial_tabs[0])
        
    @allure.step("Кликнуть по кнопке 'TikTok' и проверить открытие новой вкладки")
    def click_tiktok_button(self):
        """
        Кликает по кнопке TikTok и проверяет открытие новой вкладки.
        """
        from configuration.ConfigProvider import ConfigProvider
        config = ConfigProvider()
        expected_url_part = config.get_social_link("tiktok_url")

        initial_tabs = self.__driver.window_handles 

        try:
            tiktok_button = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//span[contains(@class, 'CustomMenuSocialLinksTitle') and text()='TikTok']"
                ))
            )
            tiktok_button.click()

            WebDriverWait(self.__driver, 10).until(lambda driver: len(driver.window_handles) > len(initial_tabs))

            new_tabs = self.__driver.window_handles
            new_tab = list(set(new_tabs) - set(initial_tabs))[0]
            self.__driver.switch_to.window(new_tab)

            current_url = self.__driver.current_url
            assert expected_url_part in current_url, f"Ожидали URL '{expected_url_part}', получили '{current_url}'"

            allure.attach(self.__driver.get_screenshot_as_png(), name="tiktok_tab_opened", attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            allure.attach(self.__driver.get_screenshot_as_png(), name="tiktok_tab_error", attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Ошибка при открытии TikTok: {e}")

        finally:
            if len(self.__driver.window_handles) > len(initial_tabs):
                self.__driver.close()
                self.__driver.switch_to.window(initial_tabs[0])


    @allure.step("Кликнуть по кнопке 'YouTube' и проверить открытие новой вкладки")
    def click_youtube_button(self):
        """
        Кликает по кнопке YouTube и проверяет открытие новой вкладки.
        """
        from configuration.ConfigProvider import ConfigProvider
        config = ConfigProvider()
        expected_url_part = config.get_social_link("youtube_url")

        initial_tabs = self.__driver.window_handles  

        try:
            youtube_button = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//span[contains(@class, 'CustomMenuSocialLinksTitle') and text()='YouTube']"
                ))
            )
            youtube_button.click()

            WebDriverWait(self.__driver, 10).until(lambda driver: len(driver.window_handles) > len(initial_tabs))

            new_tabs = self.__driver.window_handles
            new_tab = list(set(new_tabs) - set(initial_tabs))[0]
            self.__driver.switch_to.window(new_tab)

            current_url = self.__driver.current_url
            assert expected_url_part in current_url, f"Ожидали URL '{expected_url_part}', получили '{current_url}'"

            allure.attach(self.__driver.get_screenshot_as_png(), name="youtube_tab_opened", attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            allure.attach(self.__driver.get_screenshot_as_png(), name="youtube_tab_error", attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Ошибка при открытии YouTube: {e}")

        finally:
            if len(self.__driver.window_handles) > len(initial_tabs):
                self.__driver.close()
                self.__driver.switch_to.window(initial_tabs[0])

    @allure.step("Проверяем, открылась ли новая вкладка")
    def is_new_tab_opened(self):
        """
        Проверяет, открыта ли новая вкладка в браузере.
        Возвращает True, если количество открытых вкладок больше 1.
        """
        return len(self.__driver.window_handles) > 1
