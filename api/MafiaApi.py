import allure
import requests
import json
from pathlib import Path

class MafiaApi:
    """
    Этот класс предоставляет методы для выполнения действий с API
    """

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token

    @allure.step("Получить список юзеров")
    def get_users(self):
        path = f"{self.base_url}/user/"
        params = {
            "accessToken": self.token
    }

        resp = requests.get(path, params=params)

        print(f"Status Code: {resp.status_code}, Response Text: {resp.text}")

        try:
            return resp.json()
        except json.JSONDecodeError:
            raise ValueError(f"Ошибка декодирования JSON. Ответ API: {resp.text}")
        
    @allure.step("Получить данные юзера по ID")
    def get_user_by_ID(self, user_id):
        if not user_id:
            raise ValueError("user_id не может быть пустым или None")

        path = f"{self.base_url}/user/{user_id}"
        headers = {"Authorization": f"Bearer {self.token}"}
    
        resp = requests.get(path, headers=headers)

        print(f"Status Code: {resp.status_code}, Response Text: {resp.text}")

        try:
            return resp.json()
        except json.JSONDecodeError:
            raise ValueError(f"Ошибка декодирования JSON. Ответ API: {resp.text}")

    @allure.step("Авторизоваться")
    def auth_user(self, email, password):
        body = {
        "email": email,
        "password": password
    }
        
        path = f"{self.base_url}/auth/login"
        headers = {"Authorization": f"Bearer {self.token}"}

        resp = requests.post(path, json=body, headers=headers)

        print(f"Status Code: {resp.status_code}, Response Text: {resp.text}")

        try:
            return resp.json()
        except json.JSONDecodeError:
            raise ValueError(f"Ошибка декодирования JSON. Ответ API: {resp.text}")

    @allure.step("Создать нового юзера")    
    def create_user(self, accountType, email, name, password):
        body = {
        "accountType": accountType,
        "email": email,
        "name": name,
        "password": password
    }
    
        path = f"{self.base_url}/auth/register"
        headers = {"Authorization": f"Bearer {self.token}"}

        resp = requests.put(path, json=body, headers=headers)

        if resp.status_code != 201:
            return {"error": f"Ошибка {resp.status_code}: {resp.text}"}
        
        response_json = resp.json()

        if 'id' not in response_json:
            return {"error": "ID пользователя не найден в ответе API", "response": response_json}

        return resp.json()
    
    @allure.step("Сменить имя/обращение юзеру")
    def edit_name_pronouns(self, id, new_name, pronouns):
        body = {
        "id": id,
        "name": new_name,
        "pronouns": pronouns
    }
    
        path = f"{self.base_url}/user"
        headers = {"Authorization": f"Bearer {self.token}"}

        resp = requests.patch(path, json=body, headers=headers)

        if resp.status_code not in [200, 204]:
            return {"error": f"Ошибка {resp.status_code}: {resp.text}"}

        return resp.json() if resp.text else {}

    @allure.step("Отправить запрос на сброс пароля из личного кабинета")
    def reset_password(self, email):
        body = {
            "email": email,
            "flow": "RESET_PASSWORD"
        }

        path = f"{self.base_url}/user/sendResetPassword"
        headers = {"Authorization": f"Bearer {self.token}"}

        resp = requests.post(path, json=body, headers=headers)

        return resp.status_code, resp.json() if resp.text else {}
    
    @allure.step("Получить список Stripe Tariffs и сохранить в test_data.json")
    def get_stripe_tariffs(self):
        """
        Получает данные тарифов из Stripe и сохраняет их в test_data.json в блок 'TARIFFS'
        """
        path = f"{self.base_url}/subscriptions/currentStripeTariff"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(path, headers=headers)

        allure.attach(str(response.status_code), name="HTTP Status Code", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="Stripe Tariffs Response", attachment_type=allure.attachment_type.JSON)

        if response.status_code != 200:
            raise AssertionError(f"Ошибка {response.status_code}: {response.text}")

        try:
            tariffs_data = response.json()
        except json.JSONDecodeError:
            raise ValueError(f"Ошибка декодирования JSON. Ответ API: {response.text}")

        file_path = Path(__file__).resolve().parent.parent / "test_data.json"

        
        with file_path.open("r", encoding="utf-8") as file:
            current_data = json.load(file)

        current_data["TARIFFS"] = tariffs_data

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(current_data, file, indent=2, ensure_ascii=False)

        return tariffs_data
    
    @allure.step("Отправить запрос на оформление подписки")
    def subscribe(self, customerId, priceId):
        body = {
            'customerId': customerId,
            'priceId': priceId
        }
        path = f"{self.base_url}/subscriptions/getCheckoutSession"
        headers = {"Authorization": f"Bearer {self.token}"}
        resp = requests.post(path, json=body, headers=headers)

        if resp.status_code != 201:
            return {"error": f"Ошибка {resp.status_code}: {resp.text}"}

        return resp.json() 