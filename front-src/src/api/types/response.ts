export interface SuccessResponse<T = void> {
  code: string
  msg: string
  data?: T
}

export interface ErrorResponse {
  detail: string
}

export type ApiResponse<T = void> =
  | (SuccessResponse<T> & { success: true })
  | (ErrorResponse & { success: false })

export interface captchaItem {
  captchaId: string
  captchaCode?: string
  captchaImgBase64: string
}

export interface tokenItem {
  access_token: string
  refresh_token: string
}
