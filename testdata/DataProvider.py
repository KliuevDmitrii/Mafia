import json


my_file = open('test_data.json')
global_data = json.load(my_file)

class DataProvider:

    def __init__(self) -> None:
        self.data = global_data
        
    def get(self, prop: str, default=None) -> str:
        """Получить строковое значение параметра, вернуть default, если параметр отсутствует."""
        return self.data.get(prop, default)

    def getint(self, prop: str, default=0) -> int:
        """Получить целочисленное значение параметра, вернуть default, если параметр отсутствует."""
        try:
            return int(self.data.get(prop, default))
        except (ValueError, TypeError):
            print(f"Ошибка преобразования {prop} в int, возвращаю {default}")

    def get_token(self) -> str:
        """Получить токен."""
        return self.get("token")
    
    def set_customer_id(self, customer_id: str):
        """Сохраняет customer_id в файл test_data.json в секцию STRIPE"""
        self.data.setdefault("STRIPE", {})["customer_id"] = customer_id
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get_stripe_token(self) -> str:
        """Получить токен для Stripe."""
        return self.data.get("STRIPE", {}).get("token", "")
    
    def get_stripe_key(self) -> str:
        """Получить ключ для Stripe."""
        return self.data.get("STRIPE", {}).get("key", "")
    
    def get_every_day_price_id(self) -> str:
        """Получить priceId для ежедневного тарифа."""
        return self.data["TARIFFS"]["everyDayStripePriceId"]

    def get_month_price_id(self) -> str:
        """Получить priceId для ежемесячного тарифа."""
        return self.data["TARIFFS"]["monthStripePriceId"]

    def get_quarter_price_id(self) -> str:
        """Получить priceId для ежеквартального тарифа."""
        return self.data["TARIFFS"]["quarterStripePriceId"]

    def get_annual_price_id(self) -> str:
        """Получить priceId для годового тарифа."""
        return self.data["TARIFFS"]["annualStripePriceId"]
    
    def get_card_data(self, card_type: str = "default") -> dict:
        """Получить данные карты по типу."""
        card = self.data.get("CARD_DATA", {}).get(card_type)
        assert card is not None, f"Карта с типом '{card_type}' не найдена в test_data.json"
        return card