##################################################### MLFLOW TESTING ########################################
from dagster import asset, op, Out, List, In # type: ignore
import pandas as pd # type: ignore
import numpy as np # type: ignore
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.ensemble import RandomForestRegressor # type: ignore
import mlflow
import logging


from datetime import datetime, timedelta 
import json
import os 



def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


@op(ins={"input_data": In()})
def mlflow_run(context, input_data):
    try:
        np.random.seed(40)

        # Read the wine-quality csv file from the URL
        csv_url = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
        data = pd.read_csv(csv_url, sep=";")

        # Split the data into training and test sets. (0.75, 0.25) split.
        train, test = train_test_split(data)

        # The predicted column is "quality" which is a scalar from [3, 9]
        train_x = train.drop(["quality"], axis=1)
        test_x = test.drop(["quality"], axis=1)
        train_y = train[["quality"]]
        test_y = test[["quality"]]

        mlflow.set_tracking_uri("http://mlflow:5000/")
        context.log.info("Running ML job with input data: %s" % input_data)
        
        with mlflow.start_run():
            rf = RandomForestRegressor(n_estimators=100, random_state=42)
            rf.fit(train_x, train_y.values.ravel())

            predicted_qualities = rf.predict(test_x)

            (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

            print("RandomForest model:")
            print("  RMSE: %s" % rmse)
            print("  MAE: %s" % mae)
            print("  R2: %s" % r2)

            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)
            mlflow.log_metric("mae", mae)

            tracking_url_type_store = mlflow.get_tracking_uri().split(':')[0]

            # Model registry does not work with file store
            if tracking_url_type_store != "file":
                mlflow.sklearn.log_model(rf, "model", registered_model_name="RandomForestWineModel")
            else:
                mlflow.sklearn.log_model(rf, "model")
    
    except Exception as e:
         pass

