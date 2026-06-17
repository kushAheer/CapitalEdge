import React, { useState, useRef } from 'react';
import { UploadCloud, File, CheckCircle, Trash2, Loader2, AlertCircle } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import Button from '../ui/Button';
import './DocumentUpload.css';

const DocumentUpload = ({ onUploadSuccess, onClearSuccess, compact = false }) => {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [isClearing, setIsClearing] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null); // null, 'success', 'error'
  const [errorMessage, setErrorMessage] = useState('');
  
  const fileInputRef = useRef(null);
  const { user } = useAuth();

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const validateFile = (selectedFile) => {
    if (selectedFile.type !== 'application/pdf') {
      setErrorMessage('Only PDF files are supported.');
      setUploadStatus('error');
      return false;
    }
    setErrorMessage('');
    return true;
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (validateFile(droppedFile)) {
        setFile(droppedFile);
        setUploadStatus(null);
      }
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (validateFile(selectedFile)) {
        setFile(selectedFile);
        setUploadStatus(null);
      }
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleUpload = async () => {
    if (!file || !user) return;

    setIsUploading(true);
    setUploadStatus(null);

    const formData = new FormData();
    formData.append('user_id', user.user_id);
    formData.append('file', file);

    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      setUploadStatus('success');
      if (onUploadSuccess) onUploadSuccess();
    } catch (error) {
      console.error('Upload error:', error);
      setErrorMessage(error.message);
      setUploadStatus('error');
    } finally {
      setIsUploading(false);
    }
  };

  const handleClear = async () => {
    if (!user) return;
    
    setIsClearing(true);
    try {
      const formData = new FormData();
      formData.append('user_id', user.user_id);
      
      const response = await fetch('/api/upload/clear', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to clear document');
      }

      setFile(null);
      setUploadStatus(null);
      if (onClearSuccess) onClearSuccess();
    } catch (error) {
      console.error('Clear error:', error);
    } finally {
      setIsClearing(false);
    }
  };

  return (
    <div className={`upload-container ${compact ? 'upload-container--compact' : 'surface-panel'}`}>
      {!compact && (
        <div className="upload-header">
          <h2>Document Knowledge Base</h2>
          <p>Upload a PDF to allow the AI to answer questions based on its content.</p>
        </div>
      )}

      {!file ? (
        <div 
          className={`dropzone ${compact ? 'dropzone--compact' : ''} ${isDragging ? 'dragging' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleUploadClick}
        >
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleFileChange} 
            accept=".pdf" 
            style={{ display: 'none' }} 
          />
          <div className="dropzone-content">
            <div className="dropzone-icon">
              <UploadCloud size={compact ? 28 : 48} />
            </div>
            <h3>{compact ? 'Drop PDF here' : 'Click or drag to upload'}</h3>
            <p>{compact ? 'PDF only · max 10MB' : 'PDF files only (max 10MB)'}</p>
          </div>
        </div>
      ) : (
        <div className="file-info-card">
          <div className="file-details">
            <div className="file-icon">
              <File size={24} />
            </div>
            <div className="file-meta">
              <span className="file-name">{file.name}</span>
              <span className="file-size">{(file.size / 1024 / 1024).toFixed(2)} MB</span>
            </div>
          </div>
          
          <div className="file-actions">
            {uploadStatus === 'success' ? (
              <div className="status-success">
                <CheckCircle size={20} />
                <span>Indexed</span>
              </div>
            ) : uploadStatus === 'error' ? (
               <div className="status-error">
                <AlertCircle size={20} />
                <span>Failed</span>
              </div>
            ) : (
              <Button 
                onClick={handleUpload} 
                disabled={isUploading}
                isLoading={isUploading}
                size="sm"
              >
                Upload & Process
              </Button>
            )}
            
            <button 
              className="btn-remove" 
              onClick={handleClear}
              disabled={isUploading || isClearing}
              title="Remove document"
            >
              {isClearing ? <Loader2 className="animate-spin" size={18} /> : <Trash2 size={18} />}
            </button>
          </div>
        </div>
      )}
      
      {uploadStatus === 'error' && errorMessage && (
        <div className="upload-error-msg animate-fade-in">
          {errorMessage}
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;
