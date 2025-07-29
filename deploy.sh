#bin/bash

git pull -r
docker compose -f docker-compose-app-only.yaml down
sudo docker compose -f docker-compose-app-only.yaml up --build -d