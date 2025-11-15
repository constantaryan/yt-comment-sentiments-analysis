import mlflow
import random

mlflow.set_tracking_uri("http://ec2-43-204-145-141.ap-south-1.compute.amazonaws.com:5000")

with mlflow.start_run():
    # let's log some random paramters
    mlflow.log_param("param1",random.randint(1,100))
    mlflow.log_param("param2",random.random())

    # let's log some random metric
    mlflow.log_metric("metric1",random.random())
    mlflow.log_metric("metric2",random.uniform(0.5,1.5))

    print("Logged random paramters and metrics")