import Rollbar from 'rollbar';

const rollbar =
  process.env.NODE_ENV === 'production'
    ? new Rollbar({
        accessToken: import.meta.env.VITE_ROLLBAR_ACCESS_TOKEN,
        captureUncaught: true,
        captureUnhandledRejections: true,
        environment: 'production',
      })
    : null;

export default rollbar;
