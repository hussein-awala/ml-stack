"""
A python script train a rfr model and use it to create a SalaryRegressionModel
"""

import os

import mlflow.pyfunc
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


class SlaryRegressionModel(mlflow.pyfunc.PythonModel):
    """
    A class wrapper for the salary regression sklearn model
    """

    def load_context(self, context: mlflow.pyfunc.PythonModelContext):
        """
        load salary base model (sklearn model)
        """
        self.base_model = mlflow.sklearn.load_model(
            context.artifacts["salary_base_model"]
        )

    def predict(self, context, model_input):
        """
        predict result using the base model
        """
        return self.base_model.predict(model_input)


if __name__ == "__main__":

    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    project_path = os.getenv("PROJECT_PATH", "./")

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("salary regression")

    with mlflow.start_run(tags={"type": "regression"}):
        df = pd.read_csv(
            os.path.join(project_path, "salary_regression_model/data/data.csv")
        )
        params = {"n_estimators": 100, "random_state": 42}
        rfr = RandomForestRegressor(**params).fit(
            X=df[["YearsExperience"]], y=df["Salary"]
        )
        mlflow.log_params(params)
        salary_base_model_info = mlflow.sklearn.log_model(
            rfr, artifact_path="salary_base_model"
        )
        mlflow.pyfunc.log_model(
            artifact_path="salary_model",
            python_model=SlaryRegressionModel(),
            artifacts={"salary_base_model": salary_base_model_info.model_uri},
            registered_model_name="salary_model",
        )
