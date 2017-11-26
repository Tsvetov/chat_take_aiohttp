FROM docker-infra.ru/python-base-web-onbuild

ENV APPLICATION_NAME chat_take_aiohttp

COPY docker/etc /etc/
