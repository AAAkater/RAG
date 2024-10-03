import type { CaptchaItem } from "@/types"
import { request } from "@/utils/request"
export const refreshCaptcha = (captcha: CaptchaItem) => {
  return request.put(`/captcha/${captcha.id}/${captcha.code}`)
}
