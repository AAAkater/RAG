export interface userLoginBody {
  username: string
  password: string
  captcha_id: string
  captcha_code: string
}

export interface userRegisterBody {
  /**
   * 邮箱
   */
  email: string
  /**
   * 邮箱验证码
   */
  email_code: string
  /**
   * 密码
   */
  password: string
}
