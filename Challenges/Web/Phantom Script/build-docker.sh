#!/bin/bash
docker rm -f web_saga_scrolls
docker build -t web_saga_scrolls .
docker run --name=web_game_capsule --rm -p1337:1337 -it web_saga_scrolls
