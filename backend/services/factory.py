from typing import Dict
from .ai.annotation import AIAnnotationService
from .ai.learning import ActiveLearningService

class ServiceFactory:
    _instances: Dict = {}
    
    @classmethod
    def get_annotation_service(cls) -> AIAnnotationService:
        if "annotation" not in cls._instances:
            cls._instances["annotation"] = AIAnnotationService()
        return cls._instances["annotation"]
    
    @classmethod
    def get_learning_service(cls) -> ActiveLearningService:
        if "learning" not in cls._instances:
            cls._instances["learning"] = ActiveLearningService()
        return cls._instances["learning"] 