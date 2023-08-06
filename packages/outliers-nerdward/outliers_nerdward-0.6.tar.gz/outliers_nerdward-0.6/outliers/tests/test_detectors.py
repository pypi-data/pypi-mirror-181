import pytest
from outliers.detectors.detection_models import DetectionModels
from outliers.detectors.pipelines import OutlierDetector
from outliers.definitions import MODEL_CONFIG_PATH
import outliers.utils.data
import numpy as np

@pytest.fixture()
def dummy_data():
    data = outliers.utils.data.create_data()
    return data

def test_data_is_numpy(dummy_data):
    assert isinstance(dummy_data, np.ndarray)

def test_data_is_large(dummy_data):
    assert len(dummy_data) > 100

@pytest.fixture()
def example_models():
    models = DetectionModels(MODEL_CONFIG_PATH)
    return models

@pytest.fixture()
def example_detector(example_models):
    model = example_models.get_models()[0]
    detector = OutlierDetector(model=model)
    return detector

def test_model_creation(example_models):
    assert example_models is not None

def test_model_get_models(example_models):
    assert example_models.get_models() is not None

def test_model_evaluation(dummy_data, example_detector):
    result = example_detector.detect(dummy_data)
    assert len(result[result == -1]) == 19
    assert len(result) == len(dummy_data)
    assert np.unique(result)[0] == -1
    assert np.unique(result)[1] == 0
