import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, FileText, MessageSquare, Lock } from 'lucide-react';

const features = [
  { icon: FileText, text: 'Upload PDFs and index them instantly' },
  { icon: MessageSquare, text: 'Ask questions grounded in your documents' },
  { icon: Lock, text: 'Private to your account — never shared' },
];

const copy = {
  login: {
    eyebrow: 'Welcome back',
    title: 'Pick up where you left off.',
    subtitle: 'Sign in to access your workspace and continue chatting with your documents.',
  },
  register: {
    eyebrow: 'Get started',
    title: 'Your documents, understood.',
    subtitle: 'Create a free account and start extracting insights from your PDFs in minutes.',
  },
};

const AuthBrandPanel = ({ variant = 'login' }) => {
  const { eyebrow, title, subtitle } = copy[variant];

  return (
    <aside className="auth-brand">
      <div className="auth-brand-inner">
        <Link to="/" className="auth-brand-logo">
          <div className="auth-brand-logo-icon">
            <Shield size={22} />
          </div>
          <span>CoinWise</span>
        </Link>

        <div className="auth-brand-content">
          <span className="auth-brand-eyebrow">{eyebrow}</span>
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </div>

        <ul className="auth-brand-features">
          {features.map(({ icon: Icon, text }) => (
            <li key={text}>
              <span className="auth-brand-feature-icon">
                <Icon size={16} />
              </span>
              {text}
            </li>
          ))}
        </ul>
      </div>

      <div className="auth-brand-glow" aria-hidden="true" />
    </aside>
  );
};

export default AuthBrandPanel;
