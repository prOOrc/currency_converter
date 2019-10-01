# Currency Converter

### Запуск сервера
```shell script
docker-compose up
```

### Запуск тестов
```shell script
docker-compose run api pytest
```

### Примеры вызовов API

#### Конвертировать валюту
```shell script
curl -X GET \
  'http://0.0.0.0:8080/convert?from=USD&to=RUB&amount=42'
```

#### Обновить базу
```shell script
curl -X POST \
  'http://0.0.0.0:8080/database?merge=1' \
  -H 'Content-Type: application/json' \
  -d '[
	{
		"from": "RUB",
		"to": "USD",
		"rate": 0.0154
	},
	{
		"from": "USD",
		"to": "RUB",
		"rate": 62.3
	},
	{
		"from": "RUB",
		"to": "EUR",
		"rate": 0.0183
	}
	,
	{
		"from": "EUR",
		"to": "RUB",
		"rate": 74.5
	}
]'
```
