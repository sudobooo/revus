import { Field } from 'react-final-form';
import styles from './FormComponent.module.css';
import FileUploadIcon from '../../../public/cloud.svg';
import { useRef } from 'react';

type PropsType = {
  onChange?: (input: any) => (e: React.ChangeEvent<HTMLInputElement>) => void;
  uploadBoxText: string;
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
  const { fieldType, name, label, onChange, uploadBoxText, ...rest } = props;

  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleUpload = () => fileInputRef.current?.click();

  const dropHandler = (ev: any) => {
    ev.preventDefault();

    if (ev.dataTransfer.items) {
      // Use DataTransferItemList interface to access the file(s)
      [...ev.dataTransfer.items].forEach((item, i) => {
        // If dropped items aren't files, reject them
        if (item.kind === 'file') {
          const file = item.getAsFile();
          console.log(`… file[${i}].name = ${file.name}`);
        }
      });
    } else {
      // Use DataTransfer interface to access the file(s)
      [...ev.dataTransfer.files].forEach((file, i) => {
        console.log(`… file[${i}].name = ${file.name}`);
      });
    }
  };

  return (
    <>
      {['file'].includes(fieldType) && (
        <Field
          name={name ?? fieldType}
          render={({ input, meta }) => {
            return (
              <div className={styles.fileUploadContainer}>
                <div className={styles.uploadBox} onDrop={dropHandler}>
                  <img
                    className={styles.fileUploadIcon}
                    src={FileUploadIcon}
                    width="80"
                    height="80"
                    alt="fileUploadIcon"
                  />
                  <div className={styles.fileNames}>{uploadBoxText}</div>
                </div>
                <div className={styles.buttons}>
                  <div className={styles.fileInputContainer}>
                    <button type="button" className={styles.fileInputLabel} onClick={handleUpload}>
                      {label}
                    </button>
                    <input
                      className={styles.fileInput}
                      name={input.name}
                      onBlur={input.onBlur}
                      onFocus={input.onFocus}
                      onChange={onChange ? onChange(input) : input.onChange}
                      ref={fileInputRef}
                      {...rest}
                    />
                    {meta.touched && meta.error && <span className={styles.error}>{meta.error}</span>}
                  </div>
                  <button className={styles.submitButton} type="submit">
                    Review
                  </button>
                </div>
              </div>
            );
          }}
        />
      )}
    </>
  );
};

export default FormComponent;
