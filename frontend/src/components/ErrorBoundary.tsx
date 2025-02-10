import React, { createContext, useContext, useEffect } from 'react';
import rollbar from '../utils/rollbar';
import { isIgnoredError, isErrorLevel } from '../utils/error';

interface ErrorContextType {
  reportError: (error: Error, info?: any) => void;
}

const ErrorContext = createContext<ErrorContextType | undefined>(undefined);

export const useError = () => {
  const context = useContext(ErrorContext);
  if (!context) {
    throw new Error('useError must be used within an ErrorProvider');
  }
  return context;
};

export const ErrorProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const reportError = (error: Error, info?: any) => {
    rollbar.error(error, info);
  };

  useEffect(() => {
    const handleError = (event: ErrorEvent) => {
      if (rollbar && !isIgnoredError(event.error) && isErrorLevel(event.error)) {
        reportError(event.error);
      }
    };
    const handleUnhandledRejection = (event: PromiseRejectionEvent) => {
      const error = new Error(event.reason);
      if (rollbar && !isIgnoredError(error) && isErrorLevel(error)) {
        reportError(error);
      }
    };

    window.addEventListener('error', handleError);
    window.addEventListener('unhandledrejection', handleUnhandledRejection);
    return () => {
      window.removeEventListener('error', handleError);
      window.removeEventListener('unhandledrejection', handleUnhandledRejection);
    };
  }, []);

  return <ErrorContext.Provider value={{ reportError }}>{children}</ErrorContext.Provider>;
};
