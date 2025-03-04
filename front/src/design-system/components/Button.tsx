import React from 'react';
import { useTheme } from '../ThemeProvider';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  size?: 'small' | 'medium' | 'large';
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'medium',
  children,
  ...props
}) => {
  const { colors } = useTheme();
  
  const baseStyles = {
    backgroundColor: variant === 'primary' ? colors.primary.main : 'transparent',
    color: variant === 'primary' ? colors.neutral.surface : colors.primary.main,
    border: variant === 'secondary' ? `1px solid ${colors.primary.main}` : 'none',
    padding: size === 'small' ? '0.5rem 1rem' : size === 'medium' ? '0.75rem 1.5rem' : '1rem 2rem',
    borderRadius: '0.5rem',
    transition: 'all 0.2s ease-in-out',
  };

  return (
    <button
      style={baseStyles}
      {...props}
    >
      {children}
    </button>
  );
}; 