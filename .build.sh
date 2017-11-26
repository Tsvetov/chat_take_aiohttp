#!/bin/sh

docker build -t "docker-infra.ru/chat_take_aiohttp:$BRANCH_NAME" .
