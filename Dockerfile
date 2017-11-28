FROM python:3

RUN git clone https://github.com/Tsvetov/chat_take_aiohttp.git

RUN pip install -r /chat_take_aiohttp/requirements.txt

RUN pip install -e /chat_take_aiohttp/

ENV SIMPLE_SETTINGS chat_take_aiohttp.settings.develop

#CMD [ "chat_take_aiohttp", "serve"]
