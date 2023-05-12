# API converter
## Установка зависимостей и настройка

```bash
poetry install
```

В файле currency_service.py в переменной token вставить свой токен с сайта http://api.coinlayer.com

```python
token = 'your_token'
API_URL = f"http://api.coinlayer.com/live?access_key={token}"
```

## Запуск

### Локально: 

```bash
poetry run python main.py
```

### Через Docker:

Соберите докер образ:

```bash
docker build -t my-application .
```

Запустите докер контейнер:

```
docker run -p 8000:8000 my-application
```

Перейти по ссылке в терминале и зайти в документацию апи по эндпоинту `/docs`, конечный адрес должен выглядеть так:

`http://127.0.0.1:8000/docs#`

## Эндпоинты

1 - `/exchange-rates` - GET запрос, который выводит актуальную информацию о валюте с внешнего апи в json формате.


```json
 {
    "id": 330,
    "code": "USDT",
    "rate": 1.004178
  },
```  

2 - `/convert` - POST запрос, который конвертирует валюту одного типа в другой.

```json
{
  "from_currency": "string",
  "to_currency": "string",
  "amount": 0
}
```
