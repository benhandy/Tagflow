import { api } from './api';

export interface AnnotationRequest {
  documentIds: string[];
  model?: 'gpt-3.5-turbo' | 'gpt-4';
}

export const annotationService = {
  async batchAnnotate(projectId: string, request: AnnotationRequest) {
    return api.post(`/api/annotations/batch/${projectId}`, request);
  },
  
  async getAnnotations(documentId: string) {
    return api.get(`/api/annotations/document/${documentId}`);
  }
}; 