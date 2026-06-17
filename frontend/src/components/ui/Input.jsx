import React, { forwardRef } from 'react';
import './Input.css';

const Input = forwardRef(({ 
  label, 
  error, 
  id, 
  className = '', 
  fullWidth = true, 
  ...props 
}, ref) => {
  const inputId = id || Math.random().toString(36).substring(7);
  const widthClass = fullWidth ? 'cw-input-full' : '';
  const errorClass = error ? 'cw-input-error-state' : '';
  
  return (
    <div className={`cw-input-wrapper ${widthClass} ${className}`}>
      {label && (
        <label htmlFor={inputId} className="cw-input-label">
          {label}
        </label>
      )}
      <div className="cw-input-container">
        <input
          ref={ref}
          id={inputId}
          className={`cw-input ${errorClass}`}
          {...props}
        />
      </div>
      {error && <p className="cw-input-error-text">{error}</p>}
    </div>
  );
});

Input.displayName = 'Input';

export default Input;
