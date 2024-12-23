import { ReactNode, useState } from 'react';
import { Form } from 'react-final-form';
import FormComponent from '../../../shared/FormComponent';

type FormValues = {
  code: File | null;
};

function ReviewCode() {
  const [review, setReview] = useState('');

  const dispatch = (res: string) => res;
  const reviewCodeThunk = (values: any) => {
    const { code } = values as { code: string | ArrayBuffer | null };
    if (!code) {
      return;
    }
    if ((code instanceof ArrayBuffer && code.byteLength > 10) || (typeof code === 'string' && code.length > 10)) {
      return 'Все отлично! Продолжай в том же духе.';
    }
    return 'Давай по новой, Миша, все хуйня!';
  };

  const onSubmit = (values: FormValues) => {
    if (!values.code) {
      return;
    }

    const reader = new FileReader();

    reader.onload = () => {
      const code: string | ArrayBuffer | null = reader.result;
      let result: string = '';
      try {
        result = reviewCodeThunk({ code }) ?? '';
        dispatch(result);
      } catch {
        return;
      }
      setReview(result);
    };

    reader.readAsText(values.code);
  };

  const onChange = (input: any) => (e: React.ChangeEvent<HTMLInputElement>) => {
    const target = e.target as HTMLInputElement;
    let file = null;

    if (target && target.files && target.files.length > 0) {
      const filesArray = Array.from(target.files);
      file = filesArray[0];
    }

    input.onChange(file);
  };
  const formComponentProps = {
    fieldType: 'file',
    type: 'file',
    name: 'code',
    label: 'Upload your code',
    onChange,
    accept: '.js,.ts,.py,.c,.java,.php,.swift,.cc,.cpp,.cxx,.cs,.rs,.go,.kt,.rb,.ex',
  };

  return (
    <Form
      onSubmit={onSubmit}
      initialValues={{ code: null }}
      render={({ handleSubmit, submitError }: { handleSubmit: () => void; submitError?: ReactNode }) => (
        <div>
          <form onSubmit={handleSubmit}>
            <FormComponent {...formComponentProps} />
            {submitError && <span>{submitError}</span>}
            <button type="submit">Review</button>
          </form>
          {review != '' && <div>{review}</div>}
        </div>
      )}
    />
  );
}

export default ReviewCode;
