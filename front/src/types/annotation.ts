export interface Annotation {
  id: string;
  content: any;
  confidence_score: number;
  created_at: string;
  document_id: string;
  verified: boolean;
}

export interface BatchAnnotationResult {
  message: string;
  annotations: Annotation[];
} 