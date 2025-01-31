export const isIgnoredError = (error: Error) => {
  const ignoredMessages = [
    'ResizeObserver loop limit exceeded',
    'Script error',
    'Non-Error promise rejection captured',
  ];

  return ignoredMessages.some((msg) => error.message.includes(msg));
};

export const isErrorLevel = (error: Error) => (error.message.includes('warning') ? false : true);
