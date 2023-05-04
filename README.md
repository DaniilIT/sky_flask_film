# Исходный код для курсовой работы №3

## Описание проекта
- Установка зависимостей
```shell
python -m pip install -r requirements.txt

python -m pip install -r requirements.dev.txt
```

- Создание моделей (очистит БД и создаст все модели, указанные в импорте)
```shell
python create_tables.py
```

- Загрузка данных в базу
```shell
python load_fixtures.py
```
Скрипт читает файл fixtures.json и загружает данные в базу. Если данные уже загружены - выводит соответсвующее сообщение. 

## Запуск проекта

### Bash (Linux/MACOS)
```shell
export FLASK_APP=run.py
export FLASK_ENV='development'
python -m flask run
```

### PowerShell (Windows)
```shell
$env:FLASK_APP = "run"
$env:FLASK_ENV = "development"
flask run
```

## Запуск тестов
```shell
python -m pytest .
```
