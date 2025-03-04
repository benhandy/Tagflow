import React from 'react';
import { useTheme } from '../ThemeProvider';

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large';
  color?: 'primary' | 'secondary';
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'medium',
  color = 'primary',
}) => {
  const { colors } = useTheme();

  const getSize = () => {
    switch (size) {
      case 'small':
        return '1rem';
      case 'large':
        return '3rem';
      default:
        return '2rem';
    }
  };

  const spinnerColor = color === 'primary' ? colors.primary.main : colors.neutral.text.secondary;

  return (
    <div
      style={{
        display: 'inline-block',
        width: getSize(),
        height: getSize(),
        border: `2px solid ${colors.neutral.border}`,
        borderTopColor: spinnerColor,
        borderRadius: '50%',
        animation: 'spin 1s linear infinite',
      }}
    />
  );
}; 