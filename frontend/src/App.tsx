import CodeReviewerForm from './components/Pages/Main/Form/index';
import styles from './index.module.css';
import { ToastContainer } from 'react-toastify';
import { ErrorProvider } from './components/ErrorBoundary';

const App = () => {
  return (
    <ErrorProvider>
      <div className={styles.container}>
        <div className={styles.h1}>Review your code with AI</div>
        <CodeReviewerForm />
        <ToastContainer position="top-right" autoClose={3000} />
      </div>
    </ErrorProvider>
  );
};

export default App;
