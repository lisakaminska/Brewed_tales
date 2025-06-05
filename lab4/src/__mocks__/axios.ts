import { AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios';

const mockAxios = {
  get: jest.fn().mockResolvedValue({ data: {} }),
  post: jest.fn().mockResolvedValue({ data: {} }),
  put: jest.fn().mockResolvedValue({ data: {} }),
  delete: jest.fn().mockResolvedValue({ data: {} }),
  create: jest.fn().mockReturnThis(),
};

export default mockAxios; 