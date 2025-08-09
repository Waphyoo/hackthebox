#!/bin/bash
docker rm -f web_feedback_flux
docker build --tag=web_feedback_flux .
docker run -p 1337:8000 --rm --name=web_feedback_flux -it web_feedback_flux