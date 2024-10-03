import axios from "axios"

export const baseApiUrl = import.meta.env.VITE_BASE_API_URL

const service = axios.create({
  baseURL: baseApiUrl,
  timeout: 10000,
})

// 请求拦截器
service.interceptors.request.use()
// 响应拦截器
service.interceptors.response.use()

export { service as request }
