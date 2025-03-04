import React from 'react';
import { Outlet } from 'react-router-dom';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { Breadcrumbs } from './Breadcrumbs';

export const Layout: React.FC = () => {
  return (
    <div className="min-h-screen bg-neutral-background">
      <Header />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">
          <Breadcrumbs />
          <div className="mt-4">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}; 