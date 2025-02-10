import axios, { AxiosResponse, AxiosError, InternalAxiosRequestConfig } from 'axios';
import { camelizeKeys, decamelizeKeys } from 'humps';

interface CustomAxiosRequestConfig extends InternalAxiosRequestConfig {
  forceMiddleware?: boolean;
}

const { VITE_NODE_ENV } = import.meta.env;
const APP_COMMIT = import.meta.env.VITE_APP_COMMIT ?? '';
const isDevelopment = VITE_NODE_ENV === 'development';
const baseApiURL = isDevelopment ? 'dev' : 'prod';

const api = axios.create({
  baseURL: baseApiURL,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
  transformResponse: [
    ...(Array.isArray(axios.defaults.transformResponse)
      ? axios.defaults.transformResponse
      : axios.defaults.transformResponse
        ? [axios.defaults.transformResponse]
        : []),
    (data: any) => camelizeKeys(data),
  ],
  transformRequest: [
    (data: any) => (data instanceof FormData ? data : decamelizeKeys(data)),
    ...(Array.isArray(axios.defaults.transformRequest)
      ? axios.defaults.transformRequest
      : axios.defaults.transformRequest
        ? [axios.defaults.transformRequest]
        : []),
  ],
});

api.interceptors.request.use((config: CustomAxiosRequestConfig | any) => {
  if (config.baseURL === baseApiURL || config.forceMiddleware) {
    config.headers['X-Commit-Version'] = APP_COMMIT;

    const url = new URL(config.baseURL + config.urlPath);
    url.searchParams.set('_v', APP_COMMIT);

    config.url = url.toString().replace(config.baseURL, '');
  }

  return config;
});

api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (axiosError: AxiosError) => {
    const error = axiosError?.response?.data || axiosError;
    if (shouldReportAxiosError(axiosError)) {
      errorTracking.sendError(error, '[axiosApi]');
    } else {
      logger.error('Axios request error: >>', error);
    }

    throw error;
  },
);

export default api;
