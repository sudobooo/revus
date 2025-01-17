import ReviewCodeForm from './components/Pages/Main/Form/index';
import styles from './index.module.css';

function App() {
  return (
    <div className={styles.container}>
      <div className={styles.h1}>Review your code with AI</div>
      <ReviewCodeForm />
    </div>
  );
}

export default App;
