import os
from src.pipeline.training_pipeline import Training_Pipeline
from src.logger import logging
from src.exception import CustomException

obj = Training_Pipeline()
obj.run_pipeline()