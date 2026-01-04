import axios from 'axios';

// 1. 创建一个实例，设置通用配置
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', // 以后改服务器地址只改这一行
});

// 2. 请求拦截器：在请求发出去之前，自动把 Token 塞进去
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 3. 响应拦截器：如果后端返回 401，说明 Token 失效了，自动处理
api.interceptors.response.use(
  (response) => response,(error) => {
    if (error.response && error.response.status === 401) {
      console.log("Token 过期或无效，请重新登录");
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      // 这里可以根据需要跳转到登录页或刷新状态
    }
    return Promise.reject(error);
  }
);

export default api;