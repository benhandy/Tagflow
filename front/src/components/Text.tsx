import React from 'react';
import classNames from 'classnames';

interface TextProps {
  variant?: 'h1' | 'h2' | 'h3' | 'body1' | 'body2' | 'caption';
  color?: 'primary' | 'secondary';
  children: React.ReactNode;
  className?: string;
}

export const Text: React.FC<TextProps> = ({
  variant = 'body1',
  color = 'primary',
  children,
  className,
}) => {
  const baseStyles = {
    'text-neutral-text-primary': color === 'primary',
    'text-neutral-text-secondary': color === 'secondary',
  };

  const variantStyles = {
    h1: 'text-4xl font-bold',
    h2: 'text-3xl font-semibold',
    h3: 'text-2xl font-medium',
    body1: 'text-base',
    body2: 'text-sm',
    caption: 'text-xs',
  };

  return (
    <span
      className={classNames(
        baseStyles,
        variantStyles[variant],
        className
      )}
    >
      {children}
    </span>
  );
}; 