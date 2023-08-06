from sagemaker.sklearn.processing import SKLearnProcessor

class SKLearnProcessorBuilder:
    """Handles Amazon SageMaker processing tasks for jobs using scikit-learn."""

    def __init__(self) -> None:
        self._instance = None

    def __call__(self) -> SKLearnProcessor:
        return self._instance