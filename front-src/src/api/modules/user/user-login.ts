import { request } from "@/utils/request"

const URL = "/session"
export const userLogin = () => {
  return request.post(URL)
}
