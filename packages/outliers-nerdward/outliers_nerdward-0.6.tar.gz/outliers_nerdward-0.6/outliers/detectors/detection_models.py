import json
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN

class DetectionModels(object):
    def __init__(self, model_config_path=None):
        if model_config_path is not None:
            with open(model_config_path) as w:
                self.model_def = json.load(w)
    
    def create_model(self, model_name=None, params=None):
        if model_name is None and params is None:
            return None
        elif model_name == 'IsolationForest' and params is not None:
            return IsolationForest(**params)
        elif model_name == 'DBSCAN' and params is not None:
            return DBSCAN(**params)
    def get_models(self):
        models = []
        for model_definition in self.model_def:
            defined_model = self.create_model(
                model_name=model_definition['model'],
                params=model_definition['params']
            )
            models.append(defined_model)
        return models
