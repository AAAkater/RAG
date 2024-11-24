import { request } from "@/utils/request"
import type { AxiosPromise } from "axios"
import { type userLoginBody, type userRegisterBody } from "../types/params"
import type { ApiResponse, tokenItem } from "../types/response"

const USER_URL = "/user"
export const userLogin = (
  userInfo: userLoginBody,
): AxiosPromise<ApiResponse<tokenItem>> => {
  return request.post("/login", userInfo)
}

export const userRegister = (
  new_user_info: userRegisterBody,
): AxiosPromise<ApiResponse> => {
  return request.post(USER_URL, new_user_info)
}
