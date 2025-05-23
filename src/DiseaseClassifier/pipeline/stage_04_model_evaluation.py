from src.DiseaseClassifier.config.configuration import ConfigurationManager
from src.DiseaseClassifier.components.model_evaluation_mlflow import Evaluation
from src.DiseaseClassifier import logger

STAGE_NAME = "Evaluation stage"

class EvaluationPipeline:
    def __init__(self):
        pass
    def main(self):               
        try:
            config = ConfigurationManager()
            evaluation_config = config.get_evaluation_config()
            evaluation = Evaluation(config=evaluation_config)
            evaluation.evaluation()
            evaluation.save_score()
            evaluation.log_into_mlflow()
        except Exception as e:
            raise e
        

if __name__ == "__main__":
    try:
        logger.info(f"**********************")
        logger.info(f">>>>>>>> stage {STAGE_NAME} started <<<<<<<")
        obj = EvaluationPipeline()
        obj.main()
        logger.info(f">>>>>>>> stage {STAGE_NAME} completed <<<<<<<\n\nx==========================x")
    except Exception as e:
        raise e