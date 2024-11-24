import type { ApiResponse, captchaItem } from "@/api/types/response"
import type { CaptchaItem } from "@/types"
import { request } from "@/utils/request"
import type { AxiosPromise } from "axios"
export const getCaptcha = (): AxiosPromise<ApiResponse<captchaItem>> => {
  return request.get(`/captcha`)
}
export const refreshCaptcha = (
  oldCaptchaId: string,
): AxiosPromise<ApiResponse<captchaItem>> => {
  return request.put(`/captcha/${oldCaptchaId}`)
}

export const verifyCaptcha = (
  captcha: CaptchaItem,
): AxiosPromise<ApiResponse> => {
  return request.post(`/captcha/${captcha.id}/${captcha.code}`)
}

export const getEmailCaptcha = (
  email_str: string,
): AxiosPromise<ApiResponse> => {
  return request.get(`/captcha/email`, {
    params: {
      email: encodeURIComponent(email_str),
    },
  })
}

export const verifyEmailCaptcha = (
  email: string,
  code: string,
): AxiosPromise<ApiResponse> => {
  return request.post(`/captcha/email`, {
    email: email,
    email_code: code,
  })
}
