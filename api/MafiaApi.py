import allure
import requests
import json

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
        
    