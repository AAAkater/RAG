import type { CaptchaItem } from "@/types"
import { request } from "@/utils/request"
export const verifyCaptcha = (captcha: CaptchaItem) => {
  return request.post(`/captcha/${captcha.id}/${captcha.code}`)
}
