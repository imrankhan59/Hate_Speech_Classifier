import mlflow
from src.utils.utils import setup_mlflow

setup_mlflow()

print(mlflow.is_tracking_uri_set())

with mlflow.start_run(run_name="test_run"):
    mlflow.log_param("param1", 5)
    mlflow.log_metric("foo", 2)
    mlflow.log_metric("foo", 3)
    mlflow.log_metric("foo", 4)