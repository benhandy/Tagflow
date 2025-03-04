import React from 'react';
import { Button } from '../design-system/components/Button';
import { Typography } from '../design-system/components/Typography';

interface AnnotationToolbarProps {
  labels: string[];
  onAnnotate: (label: string) => void;
  shortcuts?: boolean;
}

export const AnnotationToolbar: React.FC<AnnotationToolbarProps> = ({
  labels,
  onAnnotate,
  shortcuts = true
}) => {
  React.useEffect(() => {
    if (!shortcuts) return;

    const handleKeyPress = (e: KeyboardEvent) => {
      // Numbers 1-9 for quick labeling
      if (e.key >= '1' && e.key <= '9') {
        const index = parseInt(e.key) - 1;
        if (index < labels.length) {
          onAnnotate(labels[index]);
        }
      }
    };

    window.addEventListener('keypress', handleKeyPress);
    return () => window.removeEventListener('keypress', handleKeyPress);
  }, [labels, onAnnotate, shortcuts]);

  return (
    <div className="flex flex-wrap gap-2 p-4 bg-gray-50 rounded-lg">
      {labels.map((label, index) => (
        <Button
          key={label}
          variant="secondary"
          onClick={() => onAnnotate(label)}
        >
          <span className="flex items-center gap-2">
            {label}
            {shortcuts && index < 9 && (
              <kbd className="px-2 py-1 bg-gray-200 rounded text-xs">
                {index + 1}
              </kbd>
            )}
          </span>
        </Button>
      ))}
    </div>
  );
}; 