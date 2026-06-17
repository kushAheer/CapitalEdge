import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, ArrowRight, FileText, MessageSquare, Sparkles } from 'lucide-react';
import Button from '../components/ui/Button';
import './Home.css';

const Home = () => {
  return (
    <div className="home-container">
      <div className="home-bg-decoration" aria-hidden="true">
        <div className="home-bg-orb home-bg-orb--1" />
        <div className="home-bg-orb home-bg-orb--2" />
      </div>

      <main className="hero-section">
        <div className="hero-content">
          <div className="hero-badge">
            <Sparkles size={14} />
            <span>AI-powered document intelligence</span>
          </div>

          <h1 className="hero-title">
            Your documents,
            <span className="hero-title-accent"> understood.</span>
          </h1>

          <p className="hero-subtitle">
            Upload any PDF and chat with an AI that reads every page. Get precise answers grounded in your content — not the internet.
          </p>

          <div className="hero-actions">
            <Link to="/register">
              <Button size="lg" className="hero-btn">
                Get started free
                <ArrowRight size={18} className="ml-2" />
              </Button>
            </Link>
            <Link to="/login">
              <Button variant="secondary" size="lg" className="hero-btn">
                Sign in
              </Button>
            </Link>
          </div>
        </div>

        <div className="hero-preview surface-panel">
          <div className="preview-header">
            <div className="preview-dots">
              <span /><span /><span />
            </div>
            <span className="preview-label">CoinWise · Dashboard</span>
          </div>
          <div className="preview-body">
            <div className="preview-sidebar">
              <div className="preview-doc">
                <FileText size={16} />
                <div>
                  <span className="preview-doc-name">Q4_Report.pdf</span>
                  <span className="preview-doc-status">Indexed</span>
                </div>
              </div>
            </div>
            <div className="preview-chat">
              <div className="preview-msg preview-msg--user">
                What were the key revenue drivers?
              </div>
              <div className="preview-msg preview-msg--ai">
                Based on your document, the three main revenue drivers were enterprise subscriptions (+34%), API usage growth, and the new analytics tier launched in October.
              </div>
              <div className="preview-input">
                <span>Ask anything about your document…</span>
                <div className="preview-send" />
              </div>
            </div>
          </div>
        </div>
      </main>

      <section className="features-section">
        <div className="features-header">
          <h2>Everything you need to work smarter</h2>
          <p>From upload to insight in seconds — no setup required.</p>
        </div>
        <div className="features-grid">
          <div className="feature-card surface-panel">
            <div className="feature-icon feature-icon--upload">
              <FileText size={22} />
            </div>
            <h3>Upload any PDF</h3>
            <p>Drop a file and we index it instantly. Your document becomes a searchable knowledge base.</p>
          </div>

          <div className="feature-card surface-panel">
            <div className="feature-icon feature-icon--chat">
              <MessageSquare size={22} />
            </div>
            <h3>Chat with context</h3>
            <p>Ask natural questions and get answers pulled directly from your document — with full accuracy.</p>
          </div>

          <div className="feature-card surface-panel">
            <div className="feature-icon feature-icon--secure">
              <Shield size={22} />
            </div>
            <h3>Private & secure</h3>
            <p>Your files stay tied to your account. Encrypted in transit, never shared or used for training.</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
