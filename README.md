# ML Stack

## Run the docker stack
```shell
PROJECT_DIR=$(git rev-parse --show-toplevel) docker-compose -f docker-compose/jupyter.yml -f docker-compose/minio.yml -f docker-compose/mlflow.yml up -d --build
```

## Stop or destroy the stack
```shell
# to stop the services
docker-compose -f docker-compose/jupyter.yml -f docker-compose/minio.yml -f docker-compose/mlflow.yml stop
# to delete the container and the created volumes
docker-compose -f docker-compose/jupyter.yml -f docker-compose/minio.yml -f docker-compose/mlflow.yml down -v
```