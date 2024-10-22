import type { ApiResponse, captchaItem } from "@/api/types/response"
import type { CaptchaItem } from "@/types"
import { baseApiUrl, request } from "@/utils/request"
import type { AxiosPromise } from "axios"
export const getCaptcha = (): AxiosPromise<ApiResponse<captchaItem>> => {
  return request.get(`${baseApiUrl}/captcha`)
}
export const refreshCaptcha = (
  oldCaptchaId: string,
): AxiosPromise<ApiResponse<captchaItem>> => {
  return request.put(`${baseApiUrl}/captcha/${oldCaptchaId}`)
}

export const verifyCaptcha = (
  captcha: CaptchaItem,
): AxiosPromise<ApiResponse> => {
  return request.post(`${baseApiUrl}/captcha/${captcha.id}/${captcha.code}`)
}

export const getEmailCaptcha = (
  email_str: string,
): AxiosPromise<ApiResponse> => {
  return request.get(`${baseApiUrl}/captcha/email/${email_str}`)
}

export const verifyEmailCaptcha = (
  email: string,
  code: string,
): AxiosPromise<ApiResponse> => {
  return request.post(`${baseApiUrl}/captcha/email`, {
    email: email,
    email_code: code,
  })
}
