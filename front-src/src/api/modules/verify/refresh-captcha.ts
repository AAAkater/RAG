import type { CaptchaItem } from "@/types"
import { request } from "@/util/request"
export const refreshCaptcha = (captcha: CaptchaItem) => {
  return request.put(`/captcha/${captcha.id}/${captcha.code}`)
}
