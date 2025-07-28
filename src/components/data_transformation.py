import os
import re
import yaml
import sys
import string
import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from src.logger import logging
from src.exception import CustomException
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact

stemmer = nltk.SnowballStemmer("english")
nltk.download('stopwords')
stopword = set(stopwords.words('english'))

class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, 
                 data_validation_artifact: DataValidationArtifact, 
                 data_transformation_config: DataTransformationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_config = data_transformation_config

    def imbalance_data_cleaning(self, imbalance_data_file_path: str) -> pd.DataFrame:
        try:
            logging.info("reading imbalance data from file paths")
            imbalance_data = pd.read_csv(imbalance_data_file_path)
            logging.info("data read successfully")

            imbalance_data = imbalance_data.drop(columns=self.data_transformation_config.ID, axis=self.data_transformation_config.AXIS, 
                                                 inplace=self.data_transformation_config.INPLACE)
            #logging.info(f"dropped ID column from imbalance data : data shape {imbalance_data.columns}")
            logging.info(f"exited the imbalance data cleaning method with data shape.")
            return imbalance_data
        except Exception as e:
            raise CustomException(e, sys)
        
    def raw_data_cleaning(self, raw_data_file_path: str) -> pd.DataFrame:
        try:
            logging.info("reading raw data from file paths")
            raw_data = pd.read_csv(raw_data_file_path)
            logging.info("raw data read successfully")
            raw_data.drop(self.data_transformation_config.DROP_COLUMN, 
                          axis=self.data_transformation_config.AXIS, inplace=self.data_transformation_config.INPLACE)
            

            logging.info(f"dropped columns {self.data_transformation_config.DROP_COLUMN} from raw data : data shape {raw_data.columns}")
            logging.info(f"removed null values from raw data : data shape {raw_data.columns}") 

            raw_data[self.data_transformation_config.CLASS].replace({0:1}, inplace=True)
            raw_data[self.data_transformation_config.CLASS].replace({2:0}, inplace=True)

            logging.info(f"raw_data classes {raw_data[self.data_transformation_config.CLASS].unique()}")

            raw_data.rename(columns={self.data_transformation_config.CLASS: self.data_transformation_config.LABEL})

            logging.info(f"renamed class column to {self.data_transformation_config.LABEL} in raw data : data shape {raw_data.columns}")

            return raw_data
        except Exception as e:
            raise CustomException(e, sys)
        
    def text_cleaning(self, text: str) -> str:
        try:
            # Lowercase
            text = str(text).lower()

            # Remove URLs
            text = re.sub(r'https?://\S+|www\.\S+', '', text)

            # Remove HTML tags
            text = re.sub(r'<.*?>+', '', text)

            # Remove punctuation
            text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)

            # Remove newlines
            text = re.sub(r'\n', ' ', text)

            # Remove words with numbers
            text = re.sub(r'\w*\d\w*', '', text)

            # Remove extra spaces
            text = re.sub(r'\s+', ' ', text).strip()

            # Tokenize
            words = text.split()

            # Remove stopwords
            words = [w for w in words if w not in stopword]

            # Stemming
            words = [stemmer.stem(w) for w in words]

            return " ".join(words)

            logging.info(f"Exited the data_cleaning method: {words}")
        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("initiate_data_transformation method started")
            data_validation_report_file = self.data_validation_artifact.data_validation_report_file_path
            with open(data_validation_report_file, 'r') as file:
                report = yaml.safe_load(file)
            if report['STATUS'] != True:
                logging.info("Data validation failed. Cannot proceed with data transformation.")
                raise Exception("Data validation failed. Cannot proceed with data transformation.")
            logging.info(f"Data validation status {report['STATUS']}")

            logging.info("Data validation passed. Proceeding with data transformation.")
            imbalance_data_file_path = self.data_ingestion_artifact.imbalance_data_file_path
            raw_data_file_path = self.data_ingestion_artifact.raw_data_file_path

            imbalance_data = self.imbalance_data_cleaning(imbalance_data_file_path)
            raw_data = self.raw_data_cleaning(raw_data_file_path)

            logging.info("cleaned imbalance and raw data successfully")

            df = pd.concat([imbalance_data, raw_data])
            
            df[self.data_transformation_config.TWEET] = df[self.data_transformation_config.TWEET].apply(self.text_cleaning)

            os.makedirs(self.data_transformation_config.DATA_TRANSFORMATION_ARTIFACT_DIR, exist_ok=True)
            df.to_csv(self.data_transformation_config.TRANSFORMED_FILE_PATH)

            logging.info(f"transformed data saved at {self.data_transformation_config.TRANSFORMED_FILE_PATH}")

            data_transformation_artifact = DataTransformationArtifact(
                transformed_file_path = self.data_transformation_config.TRANSFORMED_FILE_PATH,
            )

            return data_transformation_artifact
            logging.info(f"concatenated imbalance and raw data : data shape {df.shape}")
        except Exception as e:
            raise CustomException(e, sys)