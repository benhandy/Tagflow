from typing import List, Dict, Any, Optional
import openai
from models import Document, Project, Annotation
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json
from enum import Enum
import numpy as np
from datetime import datetime
from .prompt_templates import PromptManager, AnnotationType

class AnnotationConfidence(Enum):
    LOW = 0.6
    MEDIUM = 0.8
    HIGH = 0.9

class AIAnnotationService:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model
        self.confidence_threshold = AnnotationConfidence.MEDIUM.value
        self.temperature = 0.3
        self.max_retries = 2
        self.prompt_manager = PromptManager()

    async def generate_system_prompt(self, project_schema: Dict) -> str:
        """Generate a context-aware system prompt using the prompt manager"""
        schema_type = project_schema.get('type', 'classification')
        labels = project_schema.get('labels', [])
        domain = project_schema.get('domain')
        examples = project_schema.get('examples', [])

        # Map schema type to AnnotationType
        task_type = {
            'classification': AnnotationType.CLASSIFICATION,
            'ner': AnnotationType.ENTITY_RECOGNITION,
            'sentiment': AnnotationType.SENTIMENT,
            'relation': AnnotationType.RELATION
        }.get(schema_type, AnnotationType.CLASSIFICATION)

        return self.prompt_manager.get_prompt(
            task_type=task_type,
            labels=labels,
            domain=domain,
            examples=examples
        )

    async def annotate_document(
        self,
        document: Document,
        project: Project,
        db: AsyncSession,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """Annotate a single document with retry logic and confidence thresholding"""
        try:
            system_prompt = await self.generate_system_prompt(project.schema)
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": document.content}
                ],
                temperature=self.temperature,
                max_tokens=1000
            )

            result = self._parse_ai_response(response.choices[0].message.content)
            
            # Apply confidence thresholding
            if self._check_confidence_threshold(result):
                # Store the successful prompt for future reference
                await self._store_successful_prompt(db, system_prompt, document, result)
                return result
            elif retry_count < self.max_retries:
                # Retry with adjusted temperature
                self.temperature -= 0.1
                return await self.annotate_document(document, project, db, retry_count + 1)
            else:
                return self._create_low_confidence_result()

        except Exception as e:
            if retry_count < self.max_retries:
                return await self.annotate_document(document, project, db, retry_count + 1)
            raise AIAnnotationError(f"Failed to annotate document after {self.max_retries} retries: {str(e)}")

    def _parse_ai_response(self, content: str) -> Dict[str, Any]:
        """Parse and validate AI response"""
        try:
            if isinstance(content, str):
                content = json.loads(content)
            
            # Normalize confidence scores
            if 'label' in content:
                content['confidence'] = float(content['confidence'])
            elif 'entities' in content:
                for entity in content['entities']:
                    entity['confidence'] = float(entity['confidence'])
            
            return content
        except json.JSONDecodeError:
            raise AIAnnotationError("Invalid JSON response from AI")

    def _check_confidence_threshold(self, result: Dict[str, Any]) -> bool:
        """Check if annotation meets confidence threshold"""
        if 'label' in result:
            return result['confidence'] >= self.confidence_threshold
        elif 'entities' in result:
            return all(
                entity['confidence'] >= self.confidence_threshold
                for entity in result['entities']
            )
        return False

    async def _store_successful_prompt(
        self,
        db: AsyncSession,
        prompt: str,
        document: Document,
        result: Dict[str, Any]
    ) -> None:
        """Store successful prompts for active learning"""
        # Implementation depends on your prompt storage model
        pass

    def _create_low_confidence_result(self) -> Dict[str, Any]:
        """Create a result indicating low confidence"""
        return {
            'label': 'uncertain',
            'confidence': 0.0,
            'needs_review': True
        }

    async def learn_from_corrections(
        self,
        db: AsyncSession,
        document_id: str,
        corrections: Dict[str, Any]
    ) -> None:
        """Update AI model based on human corrections"""
        # Fetch original annotation and document
        result = await db.execute(
            select(Annotation, Document)
            .join(Document)
            .where(Document.id == document_id)
        )
        annotation, document = result.one()

        # Store correction as training example
        await self._store_training_example(
            db,
            document.content,
            annotation.content,
            corrections
        )

        # Adjust confidence thresholds based on historical accuracy
        await self._update_confidence_thresholds(db)

    async def _store_training_example(
        self,
        db: AsyncSession,
        text: str,
        ai_annotation: Dict,
        human_correction: Dict
    ) -> None:
        """Store examples for active learning"""
        # Implementation depends on your training example storage model
        pass

    async def _update_confidence_thresholds(self, db: AsyncSession) -> None:
        """Dynamically adjust confidence thresholds based on performance"""
        # Fetch recent annotation history
        recent_annotations = await db.execute(
            select(Annotation)
            .where(Annotation.verified == True)
            .order_by(Annotation.created_at.desc())
            .limit(1000)
        )

        # Calculate accuracy at different confidence levels
        confidences = []
        accuracies = []
        for ann in recent_annotations.scalars():
            if 'confidence' in ann.content:
                confidences.append(ann.content['confidence'])
                accuracies.append(1.0 if ann.verified else 0.0)

        if confidences:
            # Update threshold based on historical performance
            confidence_matrix = np.array(list(zip(confidences, accuracies)))
            optimal_threshold = self._find_optimal_threshold(confidence_matrix)
            self.confidence_threshold = optimal_threshold

    def _find_optimal_threshold(self, confidence_matrix: np.ndarray) -> float:
        """Find optimal confidence threshold using F1 score"""
        thresholds = np.arange(0.5, 1.0, 0.05)
        best_f1 = 0
        best_threshold = 0.8  # Default

        for threshold in thresholds:
            predictions = confidence_matrix[:, 0] >= threshold
            true_labels = confidence_matrix[:, 1] > 0.5
            
            tp = np.sum((predictions == 1) & (true_labels == 1))
            fp = np.sum((predictions == 1) & (true_labels == 0))
            fn = np.sum((predictions == 0) & (true_labels == 1))
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            if f1 > best_f1:
                best_f1 = f1
                best_threshold = threshold

        return best_threshold

class AIAnnotationError(Exception):
    pass 