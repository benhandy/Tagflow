import React from 'react';
import { useBatchAnnotation } from '../contexts/BatchAnnotationContext';
import { Card } from '../design-system/components/Card';
import { Typography } from '../design-system/components/Typography';

interface SelectableDocumentProps {
  id: string;
  content: string;
  status: string;
  onClick?: () => void;
}

export const SelectableDocument: React.FC<SelectableDocumentProps> = ({
  id,
  content,
  status,
  onClick
}) => {
  const { isSelected, addDocument, removeDocument } = useBatchAnnotation();
  const selected = isSelected(id);

  const handleToggle = (e: React.MouseEvent) => {
    e.preventDefault();
    if (selected) {
      removeDocument(id);
    } else {
      addDocument(id);
    }
    onClick?.();
  };

  return (
    <Card 
      className={`
        p-4 cursor-pointer transition-all
        ${selected ? 'border-primary-main bg-primary-light/10' : ''}
      `}
      onClick={handleToggle}
    >
      <div className="flex items-start space-x-4">
        <input
          type="checkbox"
          checked={selected}
          onChange={() => {}}
          className="mt-1"
        />
        <div className="flex-1">
          <Typography variant="body1" className="mb-2">
            {content.substring(0, 100)}...
          </Typography>
          <Typography variant="caption" color="secondary">
            Status: {status}
          </Typography>
        </div>
      </div>
    </Card>
  );
}; 