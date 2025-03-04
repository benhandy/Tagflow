from typing import Dict, List, Any
from enum import Enum
import json

class AnnotationType(Enum):
    CLASSIFICATION = "classification"
    ENTITY_RECOGNITION = "entity_recognition"
    SENTIMENT = "sentiment"
    RELATION = "relation"
    SEQUENCE = "sequence"

class PromptTemplate:
    def __init__(self, task_type: AnnotationType):
        self.task_type = task_type
        self.few_shot_examples = []
        self.instruction_sets = self._get_instruction_set()

    def _get_instruction_set(self) -> Dict[str, str]:
        return {
            AnnotationType.CLASSIFICATION.value: {
                "system_role": "You are an expert text classifier with deep domain knowledge.",
                "task_description": """
                Analyze the provided text and classify it according to the given labels.
                
                Key Requirements:
                1. Only use labels from the provided list
                2. Provide a confidence score (0-1) for each classification
                3. Include reasoning for your classification
                4. If multiple labels could apply, choose the most relevant
                
                Output Format:
                {
                    "label": "selected_label",
                    "confidence": float,
                    "reasoning": "explanation",
                    "alternative_labels": ["other_possible_labels"],
                    "metadata": {
                        "text_length": int,
                        "key_terms": ["relevant_terms"]
                    }
                }
                """,
            },
            AnnotationType.ENTITY_RECOGNITION.value: {
                "system_role": "You are an expert in named entity recognition and information extraction.",
                "task_description": """
                Identify and label entities in the text according to the provided schema.
                
                Key Requirements:
                1. Identify exact entity boundaries
                2. Handle nested entities
                3. Consider context for ambiguous cases
                4. Provide confidence scores for each entity
                
                Output Format:
                {
                    "entities": [
                        {
                            "text": "extracted_text",
                            "label": "entity_type",
                            "start": int,
                            "end": int,
                            "confidence": float,
                            "context": "surrounding_text",
                            "nested_entities": [{"text": "nested", "label": "type"}]
                        }
                    ],
                    "metadata": {
                        "entity_density": float,
                        "ambiguity_score": float
                    }
                }
                """,
            },
            AnnotationType.SENTIMENT.value: {
                "system_role": "You are an expert in sentiment analysis and emotion detection.",
                "task_description": """
                Analyze the sentiment and emotional content of the text.
                
                Key Requirements:
                1. Identify primary and secondary emotions
                2. Consider context and tone
                3. Handle sarcasm and implicit sentiment
                4. Account for domain-specific language
                
                Output Format:
                {
                    "sentiment": "label",
                    "confidence": float,
                    "emotions": [
                        {"emotion": "type", "intensity": float}
                    ],
                    "aspects": [
                        {
                            "target": "aspect_term",
                            "sentiment": "label",
                            "confidence": float
                        }
                    ],
                    "metadata": {
                        "subjectivity_score": float,
                        "sarcasm_detected": boolean
                    }
                }
                """,
            },
            AnnotationType.RELATION.value: {
                "system_role": "You are an expert in relationship extraction and knowledge graph construction.",
                "task_description": """
                Identify relationships between entities in the text.
                
                Key Requirements:
                1. Extract entity pairs and their relationships
                2. Consider directional relationships
                3. Handle complex or implicit relationships
                4. Identify relationship qualifiers
                
                Output Format:
                {
                    "relations": [
                        {
                            "source": {"text": "entity1", "type": "type1"},
                            "target": {"text": "entity2", "type": "type2"},
                            "relation_type": "relationship",
                            "confidence": float,
                            "qualifiers": {"temporal": "time", "condition": "condition"}
                        }
                    ],
                    "metadata": {
                        "relation_density": float,
                        "graph_complexity": float
                    }
                }
                """,
            }
        }

    def generate_prompt(
        self,
        labels: List[str],
        examples: List[Dict[str, Any]] = None,
        domain_context: str = None
    ) -> str:
        instruction_set = self.instruction_sets[self.task_type.value]
        
        prompt_parts = [
            f"# System Role\n{instruction_set['system_role']}",
            f"# Task Description\n{instruction_set['task_description']}",
            f"# Available Labels\n{', '.join(labels)}"
        ]

        if domain_context:
            prompt_parts.append(f"# Domain Context\n{domain_context}")

        if examples:
            examples_text = "\n\n".join([
                f"Example {i+1}:\nText: {ex['text']}\nAnnotation: {json.dumps(ex['annotation'], indent=2)}"
                for i, ex in enumerate(examples[:3])
            ])
            prompt_parts.append(f"# Examples\n{examples_text}")

        prompt_parts.append("""
        # Additional Guidelines
        1. If confidence is below 0.6, mark for human review
        2. Include alternative interpretations when relevant
        3. Consider document-level context
        4. Be consistent with previous annotations
        5. Flag potential edge cases
        """)

        return "\n\n".join(prompt_parts)

    def add_example(self, text: str, annotation: Dict[str, Any]) -> None:
        """Add a few-shot example to the prompt template"""
        self.few_shot_examples.append({
            "text": text,
            "annotation": annotation
        })

class PromptManager:
    def __init__(self):
        self.templates = {
            annotation_type: PromptTemplate(annotation_type)
            for annotation_type in AnnotationType
        }
        self.domain_contexts = {}

    def get_prompt(
        self,
        task_type: AnnotationType,
        labels: List[str],
        domain: str = None,
        examples: List[Dict[str, Any]] = None
    ) -> str:
        template = self.templates[task_type]
        domain_context = self.domain_contexts.get(domain)
        return template.generate_prompt(labels, examples, domain_context)

    def add_domain_context(self, domain: str, context: str) -> None:
        """Add domain-specific context for prompts"""
        self.domain_contexts[domain] = context 