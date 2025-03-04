import { createBrowserRouter, Navigate } from 'react-router-dom';
import { Layout } from '../components/layout/Layout';
import { ProjectView } from '../views/ProjectView';
import { ProjectList } from '../views/ProjectList';
import { DocumentAnnotator } from '../components/DocumentAnnotator';
import { LoginView } from '../views/LoginView';
import { ProtectedRoute } from './ProtectedRoute';

export const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginView />
  },
  {
    path: '/',
    element: <ProtectedRoute><Layout /></ProtectedRoute>,
    children: [
      {
        index: true,
        element: <Navigate to="/projects" replace />
      },
      {
        path: 'projects',
        children: [
          {
            index: true,
            element: <ProjectList />
          },
          {
            path: ':projectId',
            element: <ProjectView />
          },
          {
            path: ':projectId/documents/:documentId',
            element: <DocumentAnnotator />
          }
        ]
      }
    ]
  }
]); 