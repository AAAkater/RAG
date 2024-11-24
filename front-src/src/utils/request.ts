import { useUserStore } from "@/stores"
import axios, {
  type AxiosError,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from "axios"
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
  // if (err.status === 500) {
  //   return Promise.reject(err)
  // }
  // const errData = err.response?.data as ErrorResponse
  // err.response!.data = { ...errData, success: false }
  // console.log(err.response?.data)
  // const originalRequest = err.config

  // 设置token的无感刷新
  // 用refresh_token去更新access_token
  // if (
  //   !err.config?.url?.endsWith("/session") &&
  //   err.response?.status === 401
  // ) {
  //   try {
  //     const resp: AxiosResponse<ApiResponse<tokenItem>> = await axios.put(
  //       "http://127.0.0.1:8000/api/v1/session",
  //       {},
  //       {
  //         headers: {
  //           Authorization: `Bearer ${userStore.refresh_token}`,
  //         },
  //       },
  //     )
  //     if (!resp.data.success) {
  //     }
  //     // 更新旧token
  //     userStore.updateToken(
  //       resp.data.data!.access_token,
  //       resp.data.data!.refresh_token,
  //     )

  //     // 重新设置原请求的token
  //     originalRequest!.headers.Authorization = `Bearer ${userStore.access_token}`

  //     return service(originalRequest!)
  //   } catch (refreshError) {
  //     // 失败切换到登录页
  //     console.log(refreshError)
  //     userStore.removeToken()
  //     router.push("/login")
  //   }
  // }
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
