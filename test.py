    data_ingestion_config = DataIngestionConfig()
    data_validation_config = DataValidationConfig()
    data_transformation_config = DataTransformationConfig()
    model_trainer_config = ModelTrainerConfig()

    data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

    data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config)
    data_validation_artifact = data_validation.initiate_data_validation()

    data_transformation = DataTransformation(data_ingestion_artifact = data_ingestion_artifact, data_validation_artifact = data_validation_artifact, data_transformation_config = data_transformation_config)
    data_transformation_artifact = data_transformation.initiate_data_transformation()

    model_trainer = ModelTrainer(data_transformation_artifact = data_transformation_artifact, model_trainer_config = model_trainer_config)
    model_trainer.initiate_model_trainer()