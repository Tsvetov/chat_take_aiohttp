# chat_take_aiohttp
чат на aiohttp

Пока стаивть так.

1. Cкачивать исходники и делать

pip install -e .
в папке проекта

2. Ставить зависимости requirements.txt

3. export SIMPLE_SETTINGS="chat_take_aiohttp.settings.develop"

3. также нужно поднять redis  и базу, напрмер постгресс.
настройки
src/chat_take_aiohttp/settings/develop.py

3. Создать в базе 3 таблички, sql тут
src/chat_take_aiohttp/contrib

4. запуск
chat_take_aiohttp serve

5. Доступен по
localhost:8000

