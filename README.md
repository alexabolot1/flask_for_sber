# Шаблон проекта Flask-RESTful API
### Основная задача проекта - получение данных из .xlsx файла (файл testData.xlsx находится в корне проекта) и передача ответа клиенту в виде JSON.
**1) Структура проекта:**
* __docker-compose.yml__ - файл для запуска контейнера с БД (PostgreSQL)
* __main.py__ - файл, в котором указаны настройки приложения, создана модель БД, созданы необходимые представления
* __resource__ - файл с ресурсами для представления данных в виде JSON
* __testData.xlsx__ - файл с импортируемыми данными

**2) Инструкция по запуску:**
* Из домашней дириктории выполните:
`docker-compose up --build` - создаем образ, запускаем контейнер
* Запуск проекта:
 `python main.py`
