import React, { useState } from 'react';
import { useBatchAnnotation } from '../contexts/BatchAnnotationContext';
import { annotationService } from '../services/annotation';
import { Button } from '../design-system/components/Button';
import { Alert } from '../design-system/components/Alert';
import { LoadingSpinner } from '../design-system/components/LoadingSpinner';
import { Typography } from '../design-system/components/Typography';
import { Card } from '../design-system/components/Card';

interface BatchAnnotationPanelProps {
  projectId: string;
  onComplete?: () => void;
}

export const BatchAnnotationPanel: React.FC<BatchAnnotationPanelProps> = ({
  projectId,
  onComplete
}) => {
  const { selectedDocuments, clearSelection } = useBatchAnnotation();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [model, setModel] = useState<'gpt-3.5-turbo' | 'gpt-4'>('gpt-3.5-turbo');

  const handleAnnotate = async () => {
    if (selectedDocuments.length === 0) {
      setError('Please select documents to annotate');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      await annotationService.batchAnnotate(projectId, {
        documentIds: selectedDocuments,
        model
      });
      clearSelection();
      onComplete?.();
    } catch (err) {
      setError('Failed to annotate documents. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="p-4 mb-4">
      <div className="space-y-4">
        <Typography variant="h3">Batch Annotation</Typography>
        
        <div className="flex items-center space-x-4">
          <Typography variant="body2">
            Selected: {selectedDocuments.length} documents
          </Typography>
          
          <select
            value={model}
            onChange={(e) => setModel(e.target.value as typeof model)}
            className="px-2 py-1 border rounded"
          >
            <option value="gpt-3.5-turbo">GPT-3.5</option>
            <option value="gpt-4">GPT-4</option>
          </select>
        </div>

        {error && (
          <Alert 
            variant="error" 
            message={error}
            onClose={() => setError(null)}
          />
        )}

        <div className="flex space-x-4">
          <Button
            variant="primary"
            onClick={handleAnnotate}
            disabled={loading || selectedDocuments.length === 0}
          >
            {loading ? <LoadingSpinner size="small" /> : 'Annotate Selected'}
          </Button>

          <Button
            variant="secondary"
            onClick={clearSelection}
            disabled={loading || selectedDocuments.length === 0}
          >
            Clear Selection
          </Button>
        </div>
      </div>
    </Card>
  );
}; 