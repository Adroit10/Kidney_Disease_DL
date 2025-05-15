import os
from box.exceptions import BoxValueError
import yaml
import base64
import json
import joblib
from src.DiseaseClassifier import logger
from ensure import ensure_annotations
from box import ConfigBox
from typing import Any
from pathlib import Path

@ensure_annotations
def read_yaml(path_to_yaml:Path) -> ConfigBox:
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e

@ensure_annotations       
def create_directories(path_to_dirs:list,verbose=True):
    for path in path_to_dirs:
        os.makedirs(path,exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}") 

@ensure_annotations
def save_json(path:Path,data:dict):
    with open(path,'w') as f:
        json.dump(data,f,indent=4)

    logger.info(f"Json file saved at {path}")

@ensure_annotations
def load_json(path:Path) -> ConfigBox:
    # loads a json files data
    with open(path) as f:
        content = json.load(f)
    logger.info(f"Json file loaded successfully fromm : {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data:Any, path:Path):
    joblib.dump(value=data,filename=path)
    logger.info(f"binary file saved at: {path}")

@ensure_annotations
def load_bin(path:Path) -> Any:
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data

@ensure_annotations
def get_size(path:Path)->str:
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"

@ensure_annotations
def decodeImage(imgstring,fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName,'wb') as f:
        f.write(imgdata)
        f.close()

@ensure_annotations
def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath,"rb") as f:
        return base64.b64encode(f.read())