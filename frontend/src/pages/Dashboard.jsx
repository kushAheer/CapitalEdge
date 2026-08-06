import React from 'react';
import { FileText, Sparkles, MessageCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import DocumentUpload from '../components/upload/DocumentUpload';
import ChatInterface from '../components/chat/ChatInterface';
import './Dashboard.css';

const Dashboard = () => {
  const { user } = useAuth();
  const firstName = user?.name?.split(' ')[0] || 'there';

  return (
    <div className="dashboard">
      <aside className="dashboard-rail">
        <div className="rail-header">
          <div className="rail-greeting">
            <span className="rail-eyebrow">Workspace</span>
            <h1>Hi, {firstName}</h1>
          </div>
          <p className="rail-subtitle">Add a PDF to start chatting with your document.</p>
        </div>

        <div className="rail-section">
          <div className="rail-section-label">
            <FileText size={14} />
            <span>Document</span>
          </div>
          <DocumentUpload compact />
        </div>

        
      </aside>

      <section className="dashboard-workspace">
        <div className="workspace-toolbar">
          <div className="workspace-title">
            <MessageCircle size={18} />
            <span>Document chat</span>
          </div>
          <span className="workspace-status">Ready when your PDF is indexed</span>
        </div>
        <div className="workspace-chat">
          <ChatInterface embedded />
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
