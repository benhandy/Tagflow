import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../../design-system/components/Button';
import { Typography } from '../../design-system/components/Typography';

export const Header: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <header className="bg-white border-b border-neutral-border">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-2">
          <Typography variant="h3" className="text-primary-main">
            TagFlow
          </Typography>
        </Link>

        <div className="flex items-center space-x-4">
          <Typography variant="body2" color="secondary">
            {user?.email}
          </Typography>
          <Button variant="secondary" onClick={logout}>
            Logout
          </Button>
        </div>
      </div>
    </header>
  );
}; 