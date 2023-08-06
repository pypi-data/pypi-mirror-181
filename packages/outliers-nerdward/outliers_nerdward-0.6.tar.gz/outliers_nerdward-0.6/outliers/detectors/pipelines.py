import logging

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

class OutlierDetector():
    def __init__(self, model=None) -> None:
        if model is not None:
            self.model = model

        self.pipeline = make_pipeline(StandardScaler(), self.model)
    def detect(self, data):
        try:
            logging.debug("Fitting pipeline")
            # return self.pipeline.fit(data).predict(data)
            return self.pipeline.fit_predict(data)
        except Exception as e:
            logging.debug(f"fit_predict() failed with object {self.pipeline} ")
            logging.debug(e)
            print(e)