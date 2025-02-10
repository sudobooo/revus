import api from '../utils/api';

type formDataType = {
  code: File;
};

export async function reviewCode(formData: formDataType) {
  return api.post('/code/review', formData).then((res: any) => res.data);
}
