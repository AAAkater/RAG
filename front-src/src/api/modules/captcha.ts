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

export const verifyCaptcha = (captcha: CaptchaItem) => {
  return request.post(`${baseApiUrl}/captcha/${captcha.id}/${captcha.code}`)
}
