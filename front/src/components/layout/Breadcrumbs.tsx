import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Typography } from '../../design-system/components/Typography';

export const Breadcrumbs: React.FC = () => {
  const location = useLocation();
  const paths = location.pathname.split('/').filter(Boolean);

  return (
    <div className="flex items-center space-x-2">
      <Link to="/">
        <Typography variant="body2" color="secondary">
          Home
        </Typography>
      </Link>
      
      {paths.map((path, index) => {
        const isLast = index === paths.length - 1;
        const to = `/${paths.slice(0, index + 1).join('/')}`;
        
        return (
          <React.Fragment key={path}>
            <Typography variant="body2" color="secondary">/</Typography>
            {isLast ? (
              <Typography variant="body2">{path}</Typography>
            ) : (
              <Link to={to}>
                <Typography variant="body2" color="secondary">
                  {path}
                </Typography>
              </Link>
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
}; 