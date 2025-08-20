#!/usr/bin/env bash
docker run -d -p 27017:27017 mongo

# -d: Runs the container in detached mode (background)
# -p 27017:27017: Maps port 27017 on your host to port 27017 in the container."