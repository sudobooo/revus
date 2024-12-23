import { Field } from 'react-final-form';

type PropsType = {
  onChange?: (input: any) => (e: React.ChangeEvent<HTMLInputElement>) => void;
  fieldType: string;
  label: string;
  name?: string;
  type?: string;
  accept?: string;
  multiple?: boolean;
  capture?: boolean | 'user' | 'environment';
  webkitdirectory?: boolean;
};

const FormComponent = (props: PropsType) => {
  const { fieldType, name, label, onChange, ...rest } = props;

  return (
    <>
      {['file'].includes(fieldType) && (
        <Field
          name={name ?? fieldType}
          render={({ input, meta }) => {
            return (
              <div>
                <label htmlFor={input.name}>{label}</label>
                <input
                  name={input.name}
                  onBlur={input.onBlur}
                  onFocus={input.onFocus}
                  onChange={onChange ? onChange(input) : input.onChange}
                  {...rest}
                />
                {meta.touched && meta.error && <span>{meta.error}</span>}
              </div>
            );
          }}
        />
      )}
    </>
  );
};

export default FormComponent;
