import React from 'react';
import { NavLink } from 'react-router-dom';
import { Typography } from '../../design-system/components/Typography';

interface NavItem {
  label: string;
  path: string;
  icon?: React.ReactNode;
}

const navItems: NavItem[] = [
  { label: 'Projects', path: '/projects' },
  { label: 'Recent Documents', path: '/recent' },
  { label: 'Statistics', path: '/stats' },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-white border-r border-neutral-border p-4">
      <nav className="space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => `
              block px-4 py-2 rounded-lg transition-colors
              ${isActive ? 'bg-primary-light text-primary-main' : 'text-neutral-text-secondary hover:bg-neutral-background'}
            `}
          >
            <Typography variant="body2">
              {item.label}
            </Typography>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}; 