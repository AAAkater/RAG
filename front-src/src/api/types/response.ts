export interface SuccessResponse<T = void> {
  code: string
  msg: string
  data?: T
}

export interface ErrorResponse {
  detail: string
}

// export type ApiResponse<T = void> =
//   | (SuccessResponse<T> & { success: true })
//   | (ErrorResponse & { success: false })
export type ApiResponse<T = void> = SuccessResponse<T> | ErrorResponse
export interface captchaItem {
  captchaId: string
  captchaCode?: string
  captchaImgBase64: string
}

export interface tokenItem {
  access_token: string
  token_type: string
}
