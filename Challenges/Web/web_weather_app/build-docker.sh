#!/bin/bash
docker build --tag=weather_app2 .
docker run -p 1338:88 --rm --name=weather_app2 -it weather_app2
