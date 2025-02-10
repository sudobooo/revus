import { Field, FieldInputProps } from 'react-final-form';
import styles from './FileUploadField.module.css';
import FileUploadIcon from '../../../public/cloud.svg';
import { useRef } from 'react';
import { toast } from 'react-toastify';
import { useError } from '../ErrorBoundary';

type PropsType = {
  uploadBoxTextState: { uploadBoxText: string; setUploadBoxText: React.Dispatch<React.SetStateAction<string>> };
  submitButton: JSX.Element;
  label: string;
  name: string;
  type: string;
  accept?: string;
  multiple?: boolean;
  capture?: boolean | 'user' | 'environment';
  webkitdirectory?: boolean;
};

const getFileExtension = (filename: string) => {
  const parts = filename.split('.');
  return parts.length > 1 ? parts.pop() : '';
};

const FileUploadField = (props: PropsType) => {
  const { name, label, accept, uploadBoxTextState, submitButton, ...rest } = props;

  const { uploadBoxText, setUploadBoxText } = uploadBoxTextState;

  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const { reportError } = useError();

  const acceptExtensions = accept ? accept.split(',') : [];

  const onChange = (input: FieldInputProps<any, HTMLElement>) => (e: React.ChangeEvent<HTMLInputElement>) => {
    const target = e.target as HTMLInputElement;
    let files = null;

    try {
      if (target && target.files && target.files.length > 0) {
        files = Array.from(target.files);

        const newUploadBoxText = files?.reduce(
          (acc, current) => (acc === '' ? current.name : acc + ', ' + current.name),
          '',
        );
        setUploadBoxText(newUploadBoxText);
      } else {
        setUploadBoxText('No file chosen');
      }

      input.onChange(files);
    } catch (e: any) {
      if (!e.message?.includes('file')) {
        reportError(e, { tag: 'frontend' });
      }
      setUploadBoxText('An error occurred during file upload.');
    }
  };

  const handleUpload = () => fileInputRef.current?.click();
  const handleOnDrop = (input: FieldInputProps<any, HTMLElement>) => (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();

    if (fileInputRef.current) {
      try {
        const files = Object.values(e.dataTransfer.files);
        const filteredFilesArray = files.filter((file) =>
          acceptExtensions?.includes(getFileExtension(file.name) ?? ''),
        );
        const filteredFiles = filteredFilesArray.length > 0 ? filteredFilesArray : null;

        if (!filteredFiles || filteredFilesArray.length !== files.length) {
          toast.error('Th(is/ese) file(s) extension(s) is/are not supported');
        }

        input.onChange(filteredFiles);

        if (filteredFiles) {
          const newUploadBoxText = filteredFiles.reduce(
            (acc: string, current: any) => (acc === '' ? current.name : acc + ', ' + current.name),
            '',
          );
          setUploadBoxText(newUploadBoxText);
        } else {
          setUploadBoxText('No file chosen');
        }
      } catch (e: any) {
        if (!e.message?.includes('file')) {
          reportError(e, { tag: 'frontend' });
        }
        setUploadBoxText('An error occurred during file upload.');
      }
    }
  };
  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  return (
    <Field
      name={name}
      render={({ input, meta }) => {
        return (
          <div className={styles.fileUploadContainer}>
            <div className={styles.uploadBox} onDragOver={handleDragOver} onDrop={handleOnDrop(input)}>
              <img className={styles.fileUploadIcon} src={FileUploadIcon} width="80" height="80" alt="fileUploadIcon" />
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
                  accept={accept}
                  onBlur={input.onBlur}
                  onFocus={input.onFocus}
                  onChange={onChange ? onChange(input) : input.onChange}
                  ref={fileInputRef}
                  {...rest}
                />
                {meta.touched && meta.error && <span className={styles.error}>{meta.error}</span>}
              </div>
              {submitButton}
            </div>
          </div>
        );
      }}
    />
  );
};

export default FileUploadField;
