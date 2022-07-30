# ML Stack

## Run the docker stack
```shell
PROJECT_DIR=$(git rev-parse --show-toplevel) \
docker-compose -f docker-compose/jupyter.yml -f docker-compose/minio.yml -f docker-compose/mlflow.yml up -d --build
```

## Stop or destroy the stack
```shell
# to stop the services
docker-compose -f docker-compose/jupyter.yml -f docker-compose/minio.yml -f docker-compose/mlflow.yml stop
# to delete the container and the created volumes
docker-compose -f docker-compose/jupyter.yml -f docker-compose/minio.yml -f docker-compose/mlflow.yml down -v
```

## Create and serve your first model
After deploying the docker stack, you will have a mlflow server available on `http://localhost:5000`  
To train and log the model, you can run the `salary_model.py` script, which trains a randomForestRegressor model, wraps it in a PythonModel, and logs the two models to the mlflow server.
```shell
PROJECT_PATH=$(git rev-parse --show-toplevel) \
MLFLOW_S3_ENDPOINT_URL=http://localhost:9000 \
AWS_ACCESS_KEY_ID=minio_root \
AWS_SECRET_ACCESS_KEY=minio_pass \
python salary_regression_model/salary_model.py
```
This script will create a [model](http://localhost:5000/#/models/salary_model) in the model registry, and after each execution, it will train and create a new version of this model.  
To serve and test the model, you can use the mlflow cli (replace 1 by the version you want to deploy):
```shell
MLFLOW_S3_ENDPOINT_URL=http://localhost:9000 \
AWS_ACCESS_KEY_ID=minio_root \
AWS_SECRET_ACCESS_KEY=minio_pass \
MLFLOW_TRACKING_URI=http://localhost:5000 \
mlflow models serve -m models:/salary_model/1 --no-conda -p 5001
```
Then you can query the model using the command `curl`
```shell
curl -X POST \
-H "Content-Type:application/json; format=pandas-split" \
--data '{"columns":["YearsExperience"], "data":[[1],[2],[3]]}' \
http://localhost:5001/invocations
```
