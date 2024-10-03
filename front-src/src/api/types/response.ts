export interface ApiResponse<T> {
  code: string
  msg: string
  data?: T
}
export interface captchaItem {
  captchaId: string
  captchaCode?: string
  captchaImgBase64: string
}
