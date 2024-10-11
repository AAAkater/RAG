import { request } from "@/utils/request"
import type { AxiosPromise } from "axios"
import { type userLoginBody } from "../types/params"
import type { ApiResponse, tokenItem } from "../types/response"

const USER_URL = "/session"
export const userLogin = (
  userInfo: userLoginBody,
): AxiosPromise<ApiResponse<tokenItem>> => {
  return request.post(USER_URL, userInfo)
}
export const userLogout = (): AxiosPromise<ApiResponse> => {
  return request.delete(USER_URL)
}
