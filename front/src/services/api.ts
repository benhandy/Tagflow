import axios, { AxiosInstance } from 'axios';

export class ApiClient {
  private api: AxiosInstance;
  
  constructor() {
    this.api = axios.create({
      baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add token to requests if it exists
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Handle errors globally
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(email: string, password: string) {
    const response = await this.api.post('/auth/token', {
      username: email,
      password,
    });
    const { access_token } = response.data;
    localStorage.setItem('token', access_token);
    return response.data;
  }

  async signup(userData: {
    email: string;
    password: string;
    name: string;
    role?: string;
  }) {
    const response = await this.api.post('/auth/signup', userData);
    const { access_token } = response.data;
    localStorage.setItem('token', access_token);
    return response.data;
  }

  // Project endpoints
  async getProjects() {
    return this.api.get('/projects').then(res => res.data);
  }

  async createProject(projectData: {
    name: string;
    description?: string;
    schema: any;
  }) {
    return this.api.post('/projects', projectData).then(res => res.data);
  }

  // Document endpoints
  async getProjectDocuments(projectId: string) {
    return this.api.get(`/projects/${projectId}/documents`).then(res => res.data);
  }

  async uploadDocument(projectId: string, content: string) {
    return this.api.post(`/projects/${projectId}/documents`, { content }).then(res => res.data);
  }

  // Annotation endpoints
  async createAnnotation(documentId: string) {
    return this.api.post(`/documents/${documentId}/annotate`).then(res => res.data);
  }

  async verifyAnnotation(annotationId: string, isApproved: boolean) {
    return this.api.post(`/annotations/${annotationId}/verify`, {
      is_approved: isApproved,
    }).then(res => res.data);
  }

  async getDocumentAnnotations(documentId: string) {
    return this.api.get(`/documents/${documentId}/annotations`).then(res => res.data);
  }
}

// Create a singleton instance
export const apiClient = new ApiClient(); 