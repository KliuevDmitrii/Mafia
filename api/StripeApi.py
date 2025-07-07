import allure
import requests

class StripeApi:
    """
    Этот класс предоставляет методы для выполнения действий с API Stripe
    """

    def __init__(self, base_stripe_url: str, token_stripe: str):
        self.base_url = base_stripe_url.rstrip("/")
        self.token = token_stripe

    @allure.step("Создание нового клиента в Stripe по email")
    def create_customer(self, email: str) -> dict:
        """
        Создает нового клиента в Stripe с указанным email.
        """
        url = f"{self.base_url}/customers"
        headers = {
            "Authorization": f"Bearer {self.token}",
        }
        data = {
            "email": email
        }

        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()

    @allure.step("Поиск пользователя по email в Stripe")
    def search_customer_by_email(self, email: str) -> dict:
        """
        Выполняет поиск клиента в Stripe по email.
        """
        url = f"{self.base_url}/customers/search"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        params = {"query": f"email:'{email}'"}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    @allure.step("Получение платежных методов клиента {customer_id}")
    def get_payment_methods_by_customer_id(self, customer_id: str, method_type: str = "card") -> dict:
        """
        Получает список платежных методов (по умолчанию – карты) по customer_id.
        """
        url = f"{self.base_url}/customers/{customer_id}/payment_methods"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }
        params = {
            "type": method_type
        }

        response = requests.get(url, headers=headers, params=params)
        with allure.step("Ответ Stripe по методам оплаты"):
            allure.attach(response.text, name="Stripe PaymentMethods Response", attachment_type=allure.attachment_type.JSON)
        response.raise_for_status()
        return response.json()


