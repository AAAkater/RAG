import axios, {
  type AxiosError,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from "axios"

export const baseApiUrl = "/api/v1"

const service = axios.create({
  baseURL: baseApiUrl,
  timeout: 10000,
  withCredentials: true,
})

// 请求拦截器
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    console.log(config.url)
    // console.log(config.headers)
    return config
  },
  (err: AxiosError) => {
    return Promise.reject(err)
  },
)
// 响应拦截器
service.interceptors.response.use(
  (resp: AxiosResponse) => {
    return resp
  },
  (err: AxiosError) => {
    return Promise.reject(err)
  },
)

export { service as request }
