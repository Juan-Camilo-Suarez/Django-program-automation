## Discipline program automation
### Установка и запуск проекта
1. Создать виртуальное окружение:\
```python -m venv venv```
2. Активировать виртуальное окружение:\
```venv\Scripts\activate.bat``` - для Windows \
```source venv/bin/activate``` - для Linux и MacOS
3. Установить зависимости:\
```pip install -r requirements.txt```
4. Установка pre-commit хуков для запуска линтеров перед коммитом:\
```pre-commit install```
5. Установите PostgreSQL с официального сайта
6. Применить миграции к базе данных:\
```python manage.py migrate```
7. Запуск сервера:\
```python manage.py runserver```