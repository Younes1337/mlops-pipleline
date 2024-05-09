##################################################### MLFLOW TESTING ########################################
from dagster import job
from ..ops.ml_training import mlflow_run

@job
def train_wine_model():
    mlflow_run()

