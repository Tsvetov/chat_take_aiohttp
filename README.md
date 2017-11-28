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

Как собрать из докера:

1. склонировать проект git clone https://github.com/Tsvetov/chat_take_aiohttp.git
2 в корне проекта docker-compose build
3. там же: docker-compose up
4. http://localhost:8000/ в браузере

