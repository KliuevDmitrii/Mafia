# Mafia

## Шаги
1. Склонировать проект:
```bash
git clone https://github.com/KliuevDmitrii/Mafia.git
```

2. Установить зависимости:
```bash
pip3 install -r requirements.txt
```

3. Запустить тесты:
```bash
pytest
```

4. Сгенерировать отчет:
```bash
allure generate allure-files -o allure-report
```

5. Открыть отчет:
```bash
allure open allure-report
```

---

## Стек:
- pytest
- selenium
- webdriver manager
- requests
- allure
- configparser
- json
- sqlalchemy

---

## Структура:
```
./test           # тесты
./pages          # описание страниц
./api            # хелперы для API
./db             # хелперы для DB
./configuration  # провайдер настроек
    └ test_config.ini   # файл настроек
./testdata       # провайдер тестовых данных
    └ test_data.json    # тестовые данные
```

---

## Конфигурационные файлы

### `test_config.ini`
```
[ui]  
base_url=https://dev.ludio.gg/  
timeout=4  

# chrome | ff | firefox | edge | brave
browser_name=brave
brave_path=/usr/bin/brave-browser
# или путь под Windows: C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe

[api]  
base_url=https://dev.ludio.gg/api
base_stripe_url=https://api.stripe.com/v1

[db]
db_connection_string=connection_string

[ssh]
host=host
port=port
username=name
password=password
```

### `test_data.json`
```json
{
  "INDIVIDUAL": {
    "email": "example@example.com",
    "pass": "yourpassword",
    "accessToken": "yourtoken"
  },
  "ORGANIZATION": {
    "email": "example@example.com",
    "pass": "yourpassword"
  }
}
```

> Файлы `test_config.ini` и `test_data.json` должны быть добавлены в `.gitignore`

---

## Полезные ссылки
- [Подсказка по Markdown](https://www.markdownguide.org/basic-syntax/)
- [Генератор .gitignore](https://www.toptal.com/developers/gitignore)

---

## Установка библиотек:
```bash
pip3 install pytest
pip3 install selenium
pip3 install webdriver-manager
pip3 install allure-pytest
pip install bcrypt
```
