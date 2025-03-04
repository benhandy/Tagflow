import React from 'react';
import { Link } from 'react-router-dom';

export const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex items-center">
              <span className="text-xl font-bold text-primary-main">TagFlow</span>
            </Link>
          </div>
          <div className="flex items-center">
            <Link
              to="/login"
              className="text-base font-medium text-neutral-text-secondary hover:text-neutral-text-primary"
            >
              Login
            </Link>
          </div>
        </div>
      </nav>
    </header>
  );
}; 