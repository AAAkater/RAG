import { request } from "@/utils/request"
const url = "/captcha"
export const getCaptcha = () => {
  return request.get(url)
}
