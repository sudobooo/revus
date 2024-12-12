import { ReactNode, useState } from 'react';
import { Form, Field } from 'react-final-form';

type FormValues = {
  code?: string;
};

function ReviewCode() {
  const [result, setResult] = useState('');
  const dispatch = (res: string) => res;
  const reviewCodeThunk = (values: FormValues) => {
    const { code } = values as { code: string };
    let res: string;
    if (code.length < 10) {
      res = 'Давай по новой, Миша, всё хуйня';
    } else {
      res = 'Все отлично! Продолжай в том же духе.';
    }
    return res;
  };
  return (
    <Form
      onSubmit={(values: FormValues) => {
        const review: string = reviewCodeThunk(values);
        setResult(review);
        dispatch(review);
      }}
      initialValues={{ code: '' }}
      render={({ handleSubmit, submitError }: { handleSubmit: () => void; submitError?: ReactNode }) => (
        <div>
          <form onSubmit={handleSubmit}>
            <Field name="code">
              {({ input, meta }) => (
                <div>
                  <input {...input} placeholder="Code" type="text" />
                  {meta.touched && meta.error && <span>{meta.error}</span>}
                </div>
              )}
            </Field>
            {submitError && <span>{submitError}</span>}
            <button type="submit">Review</button>
          </form>
          {result != '' && <div>{result}</div>}
        </div>
      )}
    />
  );
}

export default ReviewCode;
