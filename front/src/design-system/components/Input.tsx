import React from 'react';
import { useTheme } from '../ThemeProvider';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  fullWidth?: boolean;
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  fullWidth = false,
  className = '',
  ...props
}) => {
  const { colors } = useTheme();

  const containerStyles: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    width: fullWidth ? '100%' : 'auto',
  };

  const inputStyles: React.CSSProperties = {
    padding: '0.75rem 1rem',
    borderRadius: '0.5rem',
    border: `1px solid ${error ? colors.feedback.error : colors.neutral.border}`,
    fontSize: '1rem',
    transition: 'all 0.2s ease-in-out',
    backgroundColor: colors.neutral.surface,
    color: colors.neutral.text.primary,
  };

  const labelStyles: React.CSSProperties = {
    marginBottom: '0.5rem',
    fontSize: '0.875rem',
    color: error ? colors.feedback.error : colors.neutral.text.secondary,
  };

  const errorStyles: React.CSSProperties = {
    marginTop: '0.25rem',
    fontSize: '0.75rem',
    color: colors.feedback.error,
  };

  return (
    <div style={containerStyles}>
      {label && <label style={labelStyles}>{label}</label>}
      <input
        style={inputStyles}
        className={className}
        {...props}
      />
      {error && <span style={errorStyles}>{error}</span>}
    </div>
  );
}; 