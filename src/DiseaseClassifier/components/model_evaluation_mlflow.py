from urllib.parse import urlparse
import os,certifi
import tensorflow as tf
from pathlib import Path
os.environ["REQUESTS_CA_BUNDLE"] = os.environ["SSL_CERT_FILE"] = certifi.where()
import dagshub
import mlflow.keras
from src.DiseaseClassifier.utils.common import save_json
from src.DiseaseClassifier.entity.config_entity import EvaluationConfig


class Evaluation:
    def __init__(self,config:EvaluationConfig):
        self.config = config

    def _valid_generator(self):

        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split=0.30
        )

        dataflow_kwargs = dict(
            target_size = self.config.params_image_size[:-1],
            batch_size = self.config.params_batch_size,
            interpolation='bilinear'
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory = self.config.training_data,
            subset = 'validation',
            shuffle=False,
            **dataflow_kwargs
        )

    @staticmethod
    def load_model(path:Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path)
    
    def evaluation(self):
        self.model = self.load_model(self.config.path_of_model)
        self._valid_generator()
        self.score = self.model.evaluate(self.valid_generator)

    def save_score(self):
        scores = {'loss':self.score[0],'accuracy':self.score[1]}
        save_json(path=Path("scores.json"),data=scores)

    def log_into_mlflow(self):

        dagshub.init(repo_owner='Adroit10', repo_name='Kidney_Disease_DL', mlflow=True)
        mlflow.set_registry_uri(mlflow.get_tracking_uri())
        tracking_scheme = urlparse(mlflow.get_tracking_uri()).scheme
        with mlflow.start_run():
            mlflow.log_params(self.config.all_params)
            mlflow.log_metrics(
                {'loss':self.score[0],'accuracy':self.score[1]}
            )

        if tracking_scheme !='file':
            mlflow.keras.log_model(
                self.model,
                artifact_path='model',
                registered_model_name="VGG16Model"
            )
        else:
            mlflow.keras.log_model(self.model,"model")
