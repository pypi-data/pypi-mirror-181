import logging
import json
import argparse
import numpy as np

from .detectors.detection_models import DetectionModels
from .detectors import pipelines
from .definitions import MODEL_CONFIG_PATH


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Anomaly Detection CLI tool')
    parser.add_argument('--source', help='Specify the location of data')
    parser.add_argument('--target', default='target.json',
                        help='Specify the location to save the predictions')

    args = parser.parse_args()
    source = args.source
    target = args.target

    # data = create_data()
    data = np.loadtxt(source, delimiter=",")
    logging.info("Reading in models")
    models = DetectionModels(MODEL_CONFIG_PATH).get_models()
    logging.info("iterating over models")
    for model in models:
        logging.info("Create detector")
        detector = pipelines.OutlierDetector(model=model)
        logging.info("Detector created")
        result = detector.detect(data)
        logging.info("Result calculated")
        result = json.dumps({'results':result.tolist()})
        
        with open(target, 'w') as f:
            f.write(result)
