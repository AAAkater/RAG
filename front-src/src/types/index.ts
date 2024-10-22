interface Meta {
  type: string
  filename: string
  id: string
}

export interface AssistantContextItem {
  from: "assistant"
  data: string
  metadata: Meta[]
  success: boolean
  inquiryContent?: string
}

export interface UserContextItem {
  from: "user"
  data: string
}

export type ContextItem = AssistantContextItem | UserContextItem

export interface LoginFormState {
  username: string
  password: string
  is_remember: boolean
  captcha_code: string
}

export interface CaptchaItem {
  id: string
  code: string
  base64: string
}

export interface RegisterFormState {
  email: string
  password: string
  email_code: string
}
