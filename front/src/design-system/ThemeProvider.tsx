import React from 'react';
import { colors } from './colors';

export const ThemeContext = React.createContext({
  colors,
  // Add more theme properties as needed
});

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <ThemeContext.Provider value={{ colors }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => React.useContext(ThemeContext); 