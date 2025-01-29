import CodeReviewerForm from './components/Pages/Main/Form/index';
import styles from './index.module.css';
import { ToastContainer } from 'react-toastify';

function App() {
  return (
    <div className={styles.container}>
      <div className={styles.h1}>Review your code with AI</div>
      <CodeReviewerForm />
      <ToastContainer position="top-right" autoClose={3000} />
    </div>
  );
}

export default App;
