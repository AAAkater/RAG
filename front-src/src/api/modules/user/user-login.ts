import { request } from "@/util/request"

const URL = "/session"
export const userLogin = () => {
  return request.post(URL)
}
