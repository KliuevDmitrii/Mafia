import allure
import requests

class StripeApi:
    """
    Этот класс предоставляет методы для выполнения действий с API Stripe
    """

    def __init__(self, base_stripe_url: str, token_stripe: str, key_stripe: str):
        self.base_url = base_stripe_url.rstrip("/")
        self.token = token_stripe
        self.key = key_stripe

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
    
    @allure.step("Создание нового платежного метода (карты) в Stripe")
    def create_payment_method(self, card_data: dict, name: str, email: str) -> dict:
        """
        Создает новый платежный метод (карта) в Stripe.
        Имя и почта берутся от зарегистрированного пользователя.
        """
        url = f"{self.base_url}/payment_methods"
        headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "type": "card",
            "card[number]": card_data["number"],
            "card[exp_month]": card_data["exp_month"],
            "card[exp_year]": card_data["exp_year"],
            "card[cvc]": card_data["cvc"],
            "billing_details[name]": name,
            "billing_details[email]": email,
            "billing_details[address][country]": card_data.get("country", "")
        }
        response = requests.post(url, headers=headers, data=data)

        with allure.step("Ответ Stripe по созданию платежного метода"):
            allure.attach(response.text, name="Stripe Create Payment Method Response", attachment_type=allure.attachment_type.JSON)

        response.raise_for_status()
        return response.json()
