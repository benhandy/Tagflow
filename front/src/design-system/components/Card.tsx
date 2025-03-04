import React from 'react';
import { useTheme } from '../ThemeProvider';

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export const Card: React.FC<CardProps> = ({ children, className = '' }) => {
  const { colors } = useTheme();

  return (
    <div
      style={{
        backgroundColor: colors.neutral.surface,
        border: `1px solid ${colors.neutral.border}`,
        borderRadius: '0.5rem',
        padding: '1rem',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
      }}
      className={className}
    >
      {children}
    </div>
  );
}; 