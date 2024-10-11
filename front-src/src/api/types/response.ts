export interface ApiResponse<T = void> {
  code: string
  msg: string
  data?: T
}
export interface captchaItem {
  captchaId: string
  captchaCode?: string
  captchaImgBase64: string
}

export interface tokenItem {
  access_token: string
  refresh_token: string
}
