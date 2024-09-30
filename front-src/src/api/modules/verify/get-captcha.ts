import { request } from "@/util/request"
const url = "/captcha"
export const getCaptcha = () => {
  return request.get(url)
}
