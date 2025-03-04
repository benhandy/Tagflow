import React from 'react';
import { useTheme } from '../ThemeProvider';

type TypographyVariant = 
  | 'h1' 
  | 'h2' 
  | 'h3' 
  | 'body1' 
  | 'body2' 
  | 'caption';

interface TypographyProps {
  variant?: TypographyVariant;
  children: React.ReactNode;
  color?: 'primary' | 'secondary';
  className?: string;
}

export const Typography: React.FC<TypographyProps> = ({
  variant = 'body1',
  children,
  color = 'primary',
  className = '',
}) => {
  const { colors } = useTheme();

  const styles: React.CSSProperties = {
    color: color === 'primary' ? colors.neutral.text.primary : colors.neutral.text.secondary,
    margin: 0,
    ...getVariantStyles(variant),
  };

  const Component = getComponent(variant);

  return (
    <Component style={styles} className={className}>
      {children}
    </Component>
  );
};

const getVariantStyles = (variant: TypographyVariant): React.CSSProperties => {
  switch (variant) {
    case 'h1':
      return { fontSize: '2.5rem', fontWeight: 600, lineHeight: 1.2 };
    case 'h2':
      return { fontSize: '2rem', fontWeight: 600, lineHeight: 1.3 };
    case 'h3':
      return { fontSize: '1.5rem', fontWeight: 500, lineHeight: 1.4 };
    case 'body1':
      return { fontSize: '1rem', lineHeight: 1.5 };
    case 'body2':
      return { fontSize: '0.875rem', lineHeight: 1.5 };
    case 'caption':
      return { fontSize: '0.75rem', lineHeight: 1.5 };
    default:
      return {};
  }
};

const getComponent = (variant: TypographyVariant): keyof JSX.IntrinsicElements => {
  switch (variant) {
    case 'h1':
      return 'h1';
    case 'h2':
      return 'h2';
    case 'h3':
      return 'h3';
    default:
      return 'p';
  }
}; 