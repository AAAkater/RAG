import { useUserStore } from "@/stores"
import axios, {
  type AxiosError,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from "axios"
import { emitter } from "./evenEmitter"
// import { useRouter } from "vue-router"

const successRequestHandler = (config: InternalAxiosRequestConfig) => {
  // 请求拦截器添加token
  if (userStore.tokenExists()) {
    config.headers.Authorization = `Bearer ${userStore.access_token}`
  }
  return config
}
const errorRequestHandler = (err: AxiosError) => {
  return Promise.reject(err)
}

const successResponseHandler = (resp: AxiosResponse) => {
  // if (resp.status !== 200) {
  //   return resp
  // }
  // const data = resp.data as SuccessResponse
  // resp.data = { ...data, success: true }
  // console.log(resp.data)
  return resp
}
const errorResponseHandler = async (err: AxiosError) => {
  const status = err.status!
  switch (status) {
    case 500: {
      emitter.emit("API_INTERNAL_SERVER_ERROR")
      break
    }
    case 401: {
      emitter.emit("API_UN_AUTH")
      break
    }
    default:
      break
  }
  return Promise.reject(err)
}

export const mockApiUrl = "http://127.0.0.1:4523/m1/4426654-4071958-f6f7b997"
export const baseApiUrl = "/api/v1"
// const router = useRouter()
const userStore = useUserStore()
const service = axios.create({
  baseURL: baseApiUrl,
  // baseURL: mockApiUrl,
  timeout: 10000,
})

// 请求拦截器
service.interceptors.request.use(successRequestHandler, errorRequestHandler)
// 响应拦截器
service.interceptors.response.use(successResponseHandler, errorResponseHandler)

export { service as request }
