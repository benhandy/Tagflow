import React from 'react';
import { useTheme } from '../ThemeProvider';

type AlertVariant = 'error' | 'success' | 'warning';

interface AlertProps {
  variant: AlertVariant;
  message: string;
  onClose?: () => void;
}

export const Alert: React.FC<AlertProps> = ({
  variant,
  message,
  onClose,
}) => {
  const { colors } = useTheme();

  const getVariantColors = (variant: AlertVariant) => {
    switch (variant) {
      case 'error':
        return {
          bg: `${colors.feedback.error}15`,
          border: colors.feedback.error,
          text: colors.feedback.error,
        };
      case 'success':
        return {
          bg: `${colors.feedback.success}15`,
          border: colors.feedback.success,
          text: colors.feedback.success,
        };
      case 'warning':
        return {
          bg: `${colors.feedback.warning}15`,
          border: colors.feedback.warning,
          text: colors.feedback.warning,
        };
    }
  };

  const variantColors = getVariantColors(variant);

  return (
    <div
      style={{
        padding: '1rem',
        borderRadius: '0.5rem',
        backgroundColor: variantColors.bg,
        border: `1px solid ${variantColors.border}`,
        color: variantColors.text,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
      }}
    >
      <span>{message}</span>
      {onClose && (
        <button
          onClick={onClose}
          style={{
            background: 'none',
            border: 'none',
            color: variantColors.text,
            cursor: 'pointer',
            padding: '0.25rem',
          }}
        >
          ✕
        </button>
      )}
    </div>
  );
}; 