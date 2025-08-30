import os 
import sys
import keras 
import pickle
import mlflow
import pandas as pd
import re
import string

import nltk
from nltk.corpus import stopwords

from src.utils.utils import setup_mlflow
from src.exception import CustomException
from src.logger import logging
from src.constant import *

from keras.utils import pad_sequences

stemmer = nltk.SnowballStemmer("english")
nltk.download('stopwords')
stopword = set(stopwords.words('english'))




class PredictionPipeline:
    def __init__(self):
        setup_mlflow()  # sets tracking URI and experiment
        self.model = None
        self.tokenizer = None
        self._load_model_and_tokenizer()

    def _load_model_and_tokenizer(self):
        try:
            """
            Load the latest Production model from MLflow and tokenizer
            """

            logging.info(f"Fetchin g Production model from MLflow {PROD_MODEL_NAME}")
            print(f"Fetching Production model: {PROD_MODEL_NAME}")

            # MLflow model URI for Production version
            prod_model_uri = f"models:/{PROD_MODEL_NAME}/Production"

            # Load model from MLflow registry
            self.model = mlflow.keras.load_model(prod_model_uri)
            logging.info("Model loaded successfully")

            # Load tokenizer (saved locally during training)
            logging.info("Loading tokenizer")
            with open("tokenizer.pickle", "rb") as f:
                self.tokenizer = pickle.load(f)
            logging.info("Tokenizer loaded successfully")
        except Exception as e:
            raise CustomException(e, sys) from e


    def text_cleaning(self, words: str) -> str:
        logging.info("Cleaning the text data")
        if pd.isna(words):
            return ""
        words = str(words).lower()
        words = re.sub('', '', words)
        words = re.sub(r'\d+', '', words)
        words = re.sub('https?://\S+|www\.\S+', '', words)
        words = re.sub('<.*?>+', '', words)
        words = re.sub('[%s]' % re.escape(string.punctuation), '', words)
        words = re.sub('\n', '', words)
        words = re.sub('\w*\d\w*', '', words)
        words = [w for w in words.split(' ') if w not in stopword]
        words = " ".join(words)
        words = [stemmer.stem(w) for w in words.split(' ')]
        words = " ".join(words)
        logging.info("Text data cleaned successfully")
        return words



    def predict(self, texts):
        try:
            """
            Run prediction on input texts
            """
            if self.model is None or self.tokenizer is None:
                raise Exception("Model or tokenizer not loaded")

            # Ensure input is list
            if isinstance(texts, str):
                texts = [texts]

            # Preprocess
            sequences = self.tokenizer.texts_to_sequences(texts)
            padded = pad_sequences(sequences, maxlen=MAX_LEN)

            preds = self.model.predict(padded)
            results = [1 if p[0] >= 0.5 else 0 for p in preds]

            return results
        except Exception as e:
            raise CustomException(e, sys)
    

if __name__ == "__main__":
    predictor = PredictionPipeline()

    sample_texts = "the product was great and I loved it"

    clean_text = predictor.text_cleaning(sample_texts)

    pred = predictor.predict(clean_text)
    print(pred) 


