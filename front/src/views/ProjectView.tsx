import React, { useEffect, useState } from 'react';
import { BatchAnnotationProvider } from '../contexts/BatchAnnotationContext';
import { BatchAnnotationPanel } from '../components/BatchAnnotationPanel';
import { SelectableDocument } from '../components/SelectableDocument';
import { DocumentAnnotator } from '../components/DocumentAnnotator';
import { Typography } from '../design-system/components/Typography';
import { LoadingSpinner } from '../design-system/components/LoadingSpinner';

interface Document {
  id: string;
  content: string;
  status: string;
}

export const ProjectView: React.FC<{ projectId: string }> = ({ projectId }) => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(null);

  const loadDocuments = async () => {
    // Implement document loading logic
  };

  useEffect(() => {
    loadDocuments();
  }, [projectId]);

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <BatchAnnotationProvider>
      <div className="space-y-6">
        <Typography variant="h2">Project Documents</Typography>
        
        <BatchAnnotationPanel 
          projectId={projectId}
          onComplete={loadDocuments}
        />

        {selectedDocument ? (
          <DocumentAnnotator
            document={selectedDocument}
            projectSchema={project.schema}
            onSave={async (annotations) => {
              // Implement save logic
              await saveAnnotations(selectedDocument.id, annotations);
              loadDocuments();
              setSelectedDocument(null);
            }}
          />
        ) : (
          <div className="space-y-4">
            {documents.map(doc => (
              <SelectableDocument
                key={doc.id}
                id={doc.id}
                content={doc.content}
                status={doc.status}
                onClick={() => setSelectedDocument(doc)}
              />
            ))}
          </div>
        )}
      </div>
    </BatchAnnotationProvider>
  );
}; 