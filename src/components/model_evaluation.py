import os
import sys 
import pickle
import numpy as np
import pandas as pd
import keras

from src.logger import logging
from src.exception import CustomException
from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artifact_entity import ModelEvaluationArtifact, ModelTrainerArtifact, DataTransformationArtifact
from src.configuration.gcloud_syncer import GCloudSyncer
from src.constant import *

from sklearn.metrics import confusion_matrix
from keras.utils import pad_sequences

class ModelEvaluation:
    def __init__(self, model_evaluation_config: ModelEvaluationConfig,
                 model_trainer_artifacts: ModelTrainerArtifact,
                 data_transformation_artifact: DataTransformationArtifact):
        self.model_evaluation_config = model_evaluation_config
        self.model_trainer_artifacts = model_trainer_artifacts
        self.data_transformation_artifacts = data_transformation_artifact
        self.gcloud = GCloudSyncer()


    def get_best_model_from_gcloud(self) ->str:
        try:
            logging.info("Entered the get_best_model_from_gcloud method of model Evaluation class")
            os.makedirs(self.model_evaluation_config.BEST_MODEL_PATH_DIR)
            self.gcloud.sync_folder_from_gcloud(self.model_evaluation_config.BUCKET_NAME,
                                                self.model_evaluation_config.MODEL_NAME,
                                                self.model_evaluation_config.BEST_MODEL_PATH_DIR)
            
            best_model_path = os.path.join(self.model_evaluation_config.BEST_MODEL_PATH_DIR, self.model_evaluation_config.MODEL_NAME)
            logging.info("Exited get_best_model_from_gcloud method of ModelEvaluation class")

            return best_model_path
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def evaluation(self, model, tokenizer):
        try:
            logging.info("Entering the evaluate method of ModelEvaluation class")
            print(self.model_trainer_artifacts.x_test_path)

            x_test = pd.read_csv(self.model_trainer_artifacts.x_test_path)
            y_test = pd.read_csv(self.model_trainer_artifacts.y_test_path)

            x_test = x_test[TWEET]
            y_test = y_test[LABEL]

            x_test = x_test.fillna("").astype(str)

            test_sequences = tokenizer.texts_to_sequences(x_test)
            test_sequences_padded = pad_sequences(test_sequences, maxlen = MAX_LEN)

            loss, accuracy = model.evaluate(test_sequences_padded, y_test)

            logging.info(f"the test accuracy is {accuracy} and {loss}")

            lstm_prediction = model.predict(test_sequences_padded)

            res = []

            for pred in lstm_prediction:
                if pred[0] < 0.5:
                    res.append(0)
                else:
                    res.append(1)

            print(confusion_matrix(y_test, res))
            logging.info(f"confusion matrix is {confusion_matrix(y_test, res)}")

            return accuracy

        except Exception as e:
            raise CustomException(e, sys)
        

    def initiate_model_evaluation(self):
        try:
            logging.info("Entering initiate_Model_Evaluation method of ModelEvaluation Class")
            logging.info("Loading current trained Model")

            trained_model = keras.models.load_model(self.model_trainer_artifacts.train_model_path)

            with open('tokenizer.pickle', 'rb') as f:
                tokenizer = pickle.load(f)

            trained_model_accuracy = self.evaluation(trained_model, tokenizer)
            logging.info(f"Trained Model accuracy {trained_model_accuracy}")

            logging.info("fetching best model from gcloud syncer")
            #best_model_path = self.get_best_model_from_gcloud()
            best_model_path = ""

            logging.info("Check is best model present in the gcloud storage or not")
            if os.path.isfile(best_model_path) is False:
                is_model_accepted = True
                logging.info("gcloud storage model is false and currently trained model accpeted is true")

            else:
                logging.info("Load best model fetched from gcloud storage")
                best_model = keras.models.load_model(best_model_path)
                best_model_accuracy = self.evaluate(tokenizer, best_model)

                logging.info("comparing loss between best_model_loss and trained_model_loss ?")

                if best_model_accuracy > trained_model_accuracy:
                    is_model_accepted = True
                    logging.info("Trained model not accepted")
                else:
                    is_model_accepted = False
                    logging.info("Trained model accepted")

            model_evaluation_artifacts = ModelEvaluationArtifact(is_model_accepted = is_model_accepted)
            return model_evaluation_artifacts
        except Exception as e:
            raise CustomException(e, sys)    