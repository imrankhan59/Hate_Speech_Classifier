import mlflow
from src.utils.utils import setup_mlflow

setup_mlflow()

with mlflow.start_run(run_name="test_run2"):
    mlflow.log_param("param1", 10)
    mlflow.log_metric("foo", 8)
    mlflow.log_metric("foo", 3)