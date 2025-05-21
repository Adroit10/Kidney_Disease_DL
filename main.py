from src.DiseaseClassifier import logger
from src.DiseaseClassifier.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from src.DiseaseClassifier.pipeline.stage_02_base_model_prep import PrepareBaseModelTrainingPipeline
from src.DiseaseClassifier.pipeline.stage_03_model_training import ModelTrainingPipeline
STAGE_NAME = "Data Ingestion stage"
try:
    logger.info(f">>>>>>>> stage {STAGE_NAME} started <<<<<<<")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f">>>>>>>> stage {STAGE_NAME} completed <<<<<<<\n\nx================x")
except Exception as e:
    raise e

STAGE_NAME = "Prepare base model"
try:
    logger.info(f">>>>>>>> stage {STAGE_NAME} started <<<<<<<")
    base_model = PrepareBaseModelTrainingPipeline()
    base_model.main()
    logger.info(f">>>>>>>> stage {STAGE_NAME} completed <<<<<<<\n\nx==========================x")
except Exception as e:
    raise e

STAGE_NAME = "Training"
try:
    logger.info(f"**********************")
    logger.info(f">>>>>>>> stage {STAGE_NAME} started <<<<<<<")
    model_trainer = ModelTrainingPipeline()
    model_trainer.main()
    logger.info(f">>>>>>>> stage {STAGE_NAME} completed <<<<<<<\n\nx==========================x")
except Exception as e:
    raise e
