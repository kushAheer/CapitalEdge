import React from 'react';
import { Link, NavLink, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { LogOut, Shield, LayoutDashboard } from 'lucide-react';
import Button from '../ui/Button';
import './Navbar.css';

const getInitials = (name) => {
  if (!name) return 'U';
  return name
    .split(' ')
    .map((part) => part[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();
};

const Navbar = () => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const isAuthPage = ['/login', '/register'].includes(location.pathname);

  return (
    <header className={`navbar ${isAuthPage ? 'navbar--auth' : ''}`}>
      <div className="navbar-inner">
        <Link to="/" className="navbar-brand">
          <div className="navbar-logo">
            <Shield size={20} />
          </div>
          <div className="navbar-brand-text">
            <span className="navbar-title">CoinWise</span>
            <span className="navbar-tagline">Document AI</span>
          </div>
        </Link>

        {user && (
          <nav className="navbar-nav" aria-label="Main">
            <NavLink
              to="/dashboard"
              className={({ isActive }) =>
                `navbar-nav-link ${isActive ? 'navbar-nav-link--active' : ''}`
              }
            >
              <LayoutDashboard size={16} />
              <span>Workspace</span>
            </NavLink>
          </nav>
        )}

        <div className="navbar-actions">
          {user ? (
            <div className="navbar-user-chip">
              <div className="navbar-user-info">
                <div className="user-avatar" aria-hidden="true">
                  {getInitials(user?.name)}
                </div>
                <div className="user-meta">
                  <span className="user-name">{user?.name || 'User'}</span>
                  <span className="user-role">Member</span>
                </div>
              </div>
              <div className="navbar-user-divider" aria-hidden="true" />
              <button
                className="navbar-logout"
                onClick={logout}
                title="Sign out"
                aria-label="Sign out"
              >
                <LogOut size={16} />
              </button>
            </div>
          ) : (
            <div className="navbar-guest-actions">
              <Link to="/login" className="navbar-link">
                Log in
              </Link>
              <Link to="/register">
                <Button size="sm">Get started</Button>
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Navbar;
