import React, { useState } from 'react';
import { Card } from '../design-system/components/Card';
import { Typography } from '../design-system/components/Typography';
import { TextSelector } from './TextSelector';
import { AnnotationToolbar } from './AnnotationToolbar';
import { Alert } from '../design-system/components/Alert';
import { LoadingSpinner } from '../design-system/components/LoadingSpinner';
import { Button } from '../design-system/components/Button';

interface DocumentAnnotatorProps {
  document: {
    id: string;
    content: string;
    annotations?: Array<{
      text: string;
      label: string;
      confidence: number;
      start: number;
      end: number;
    }>;
  };
  projectSchema: {
    labels: string[];
    type: string;
  };
  onSave: (annotations: any) => Promise<void>;
}

export const DocumentAnnotator: React.FC<DocumentAnnotatorProps> = ({
  document,
  projectSchema,
  onSave
}) => {
  const [selection, setSelection] = useState<any>(null);
  const [annotations, setAnnotations] = useState(document.annotations || []);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnnotate = async (label: string) => {
    if (!selection) return;

    const newAnnotation = {
      text: selection.text,
      label,
      confidence: 1, // Manual annotations get 100% confidence
      start: selection.start,
      end: selection.end
    };

    setAnnotations([...annotations, newAnnotation]);
    setSelection(null);
  };

  const handleSave = async () => {
    setLoading(true);
    setError(null);
    try {
      await onSave(annotations);
    } catch (err) {
      setError('Failed to save annotations');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <Typography variant="h3">Document Annotation</Typography>
        <Button
          variant="primary"
          onClick={handleSave}
          disabled={loading}
        >
          {loading ? <LoadingSpinner size="small" /> : 'Save Annotations'}
        </Button>
      </div>

      {error && (
        <Alert
          variant="error"
          message={error}
          onClose={() => setError(null)}
        />
      )}

      <AnnotationToolbar
        labels={projectSchema.labels}
        onAnnotate={handleAnnotate}
      />

      <TextSelector
        content={document.content}
        onSelection={setSelection}
        highlights={annotations}
      />

      <div className="mt-4">
        <Typography variant="h4" className="mb-2">
          Annotations ({annotations.length})
        </Typography>
        <div className="space-y-2">
          {annotations.map((ann, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-2 bg-gray-50 rounded"
            >
              <div>
                <Typography variant="body2" className="font-medium">
                  {ann.label}
                </Typography>
                <Typography variant="caption">
                  "{ann.text}"
                </Typography>
              </div>
              <Typography variant="caption">
                {Math.round(ann.confidence * 100)}% confident
              </Typography>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}; 