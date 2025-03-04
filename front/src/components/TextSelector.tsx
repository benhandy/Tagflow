import React, { useCallback, useEffect, useState } from 'react';
import { Typography } from '../design-system/components/Typography';

interface Selection {
  text: string;
  start: number;
  end: number;
}

interface TextSelectorProps {
  content: string;
  onSelection: (selection: Selection | null) => void;
  highlights?: Array<{
    start: number;
    end: number;
    label: string;
    confidence: number;
  }>;
}

export const TextSelector: React.FC<TextSelectorProps> = ({
  content,
  onSelection,
  highlights = []
}) => {
  const [currentSelection, setCurrentSelection] = useState<Selection | null>(null);

  const handleSelection = useCallback(() => {
    const selection = window.getSelection();
    if (!selection || selection.isCollapsed) {
      setCurrentSelection(null);
      onSelection(null);
      return;
    }

    const range = selection.getRangeAt(0);
    const text = selection.toString();
    
    setCurrentSelection({
      text,
      start: range.startOffset,
      end: range.endOffset
    });
    
    onSelection({
      text,
      start: range.startOffset,
      end: range.endOffset
    });
  }, [onSelection]);

  useEffect(() => {
    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, [handleSelection]);

  const renderHighlightedText = () => {
    let lastIndex = 0;
    const elements: JSX.Element[] = [];

    highlights.sort((a, b) => a.start - b.start).forEach((highlight, index) => {
      // Add text before highlight
      if (highlight.start > lastIndex) {
        elements.push(
          <span key={`text-${index}`}>
            {content.slice(lastIndex, highlight.start)}
          </span>
        );
      }

      // Add highlighted text
      elements.push(
        <mark
          key={`highlight-${index}`}
          className="bg-primary-light rounded px-1 relative group"
          style={{ backgroundColor: `rgba(59, 130, 246, ${highlight.confidence})` }}
        >
          {content.slice(highlight.start, highlight.end)}
          <span className="absolute bottom-full left-0 bg-gray-800 text-white px-2 py-1 rounded text-xs invisible group-hover:visible">
            {highlight.label} ({Math.round(highlight.confidence * 100)}%)
          </span>
        </mark>
      );

      lastIndex = highlight.end;
    });

    // Add remaining text
    if (lastIndex < content.length) {
      elements.push(
        <span key="text-final">
          {content.slice(lastIndex)}
        </span>
      );
    }

    return elements;
  };

  return (
    <div className="relative">
      <div 
        className="p-4 border rounded-lg bg-white font-mono whitespace-pre-wrap"
        style={{ userSelect: 'text' }}
      >
        {renderHighlightedText()}
      </div>
      
      {currentSelection && (
        <div className="absolute bottom-full left-0 bg-white shadow-lg rounded-lg p-2 mb-2">
          <Typography variant="caption">
            Selected: {currentSelection.text}
          </Typography>
        </div>
      )}
    </div>
  );
}; 