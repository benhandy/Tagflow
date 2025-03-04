import React, { createContext, useContext, useState } from 'react';

interface BatchAnnotationContextType {
  selectedDocuments: string[];
  addDocument: (id: string) => void;
  removeDocument: (id: string) => void;
  clearSelection: () => void;
  isSelected: (id: string) => boolean;
}

const BatchAnnotationContext = createContext<BatchAnnotationContextType | undefined>(undefined);

export const BatchAnnotationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [selectedDocuments, setSelectedDocuments] = useState<string[]>([]);

  const addDocument = (id: string) => {
    setSelectedDocuments(prev => [...prev, id]);
  };

  const removeDocument = (id: string) => {
    setSelectedDocuments(prev => prev.filter(docId => docId !== id));
  };

  const clearSelection = () => {
    setSelectedDocuments([]);
  };

  const isSelected = (id: string) => selectedDocuments.includes(id);

  return (
    <BatchAnnotationContext.Provider value={{
      selectedDocuments,
      addDocument,
      removeDocument,
      clearSelection,
      isSelected
    }}>
      {children}
    </BatchAnnotationContext.Provider>
  );
};

export const useBatchAnnotation = () => {
  const context = useContext(BatchAnnotationContext);
  if (!context) {
    throw new Error('useBatchAnnotation must be used within a BatchAnnotationProvider');
  }
  return context;
}; 