import mlflow


def setup_mlflow():
    mlflow.set_tracking_uri("http://127.0.0.1:5000") 
    mlflow.set_experiment("ML_Pipeline_Experiment")


if __name__ == "__main__":
    pass