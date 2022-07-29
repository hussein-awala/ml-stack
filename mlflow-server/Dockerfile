FROM python:3-slim

ADD requirements.txt /mlflow/
RUN pip install --no-cache-dir -r /mlflow/requirements.txt

ENV BACKEND_URI sqlite:////mlflow-db/mlflow.db
ENV ARTIFACT_ROOT /mlflow/artifacts

CMD mlflow server --backend-store-uri ${BACKEND_URI} --default-artifact-root ${ARTIFACT_ROOT} --host 0.0.0.0 --port 5000