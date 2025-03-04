from typing import List, Dict, Any
import openai
from models import Document, Project
import asyncio
from enum import Enum

class ModelType(Enum):
    GPT35 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"

class AIService:
    def __init__(self, model: ModelType = ModelType.GPT35):
        self.model = model.value
        
    async def generate_prompt(self, project_schema: Dict[str, Any], content: str) -> str:
        """Generate a context-aware prompt based on project schema"""
        schema_type = project_schema.get('type', 'classification')
        labels = project_schema.get('labels', [])
        
        prompts = {
            'classification': f"""
                Task: Classify the following text into one of these categories: {', '.join(labels)}
                Text: {content}
                Provide your response in JSON format with 'label' and 'confidence' fields.
            """,
            'entity_recognition': f"""
                Task: Identify and label entities in the following text using these labels: {', '.join(labels)}
                Text: {content}
                Provide your response in JSON format with 'entities' as a list of {{'text': '', 'label': '', 'start': 0, 'end': 0}} objects.
            """
        }
        
        return prompts.get(schema_type, prompts['classification'])

    async def annotate_document(self, document: Document, project: Project) -> Dict[str, Any]:
        """Annotate a single document using AI"""
        prompt = await self.generate_prompt(project.schema, document.content)
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert annotator. Provide annotations in the specified JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return {
                'content': response.choices[0].message.content,
                'model_version': self.model,
                'confidence_score': response.choices[0].message.get('confidence', 0.8)
            }
        except Exception as e:
            raise AIAnnotationError(f"Failed to annotate document: {str(e)}")

    async def batch_annotate(self, documents: List[Document], project: Project, batch_size: int = 5) -> List[Dict[str, Any]]:
        """Batch process documents for annotation"""
        results = []
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            tasks = [self.annotate_document(doc, project) for doc in batch]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            results.extend(batch_results)
        return results

class AIAnnotationError(Exception):
    pass 