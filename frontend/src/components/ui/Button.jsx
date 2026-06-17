import React from 'react';
import './Button.css';
import { Loader2 } from 'lucide-react';

const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  fullWidth = false,
  className = '',
  ...props
}) => {
  const baseClass = 'cw-btn';
  const variantClass = `cw-btn-${variant}`;
  const sizeClass = `cw-btn-${size}`;
  const widthClass = fullWidth ? 'cw-btn-full' : '';
  const loadingClass = isLoading ? 'cw-btn-loading' : '';

  const finalClassName = [baseClass, variantClass, sizeClass, widthClass, loadingClass, className]
    .filter(Boolean)
    .join(' ');

  return (
    <button className={finalClassName} disabled={isLoading || props.disabled} {...props}>
      {isLoading && <Loader2 className="animate-spin cw-btn-icon" size={18} />}
      <span className={isLoading ? 'cw-btn-text-hidden' : ''}>{children}</span>
    </button>
  );
};

export default Button;
