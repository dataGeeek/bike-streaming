#!/usr/bin/env bash

export ADVERTISED_HOST=$(ipconfig getifaddr en0)
docker-compose up