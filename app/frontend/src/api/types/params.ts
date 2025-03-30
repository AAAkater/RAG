export interface userLoginBody {
  /**
   * 验证码
   */
  captcha_code: string
  /**
   * 验证码id
   */
  captcha_id: string
  /**
   * 密码
   */
  password: string
  /**
   * 用户名
   */
  username: string
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
