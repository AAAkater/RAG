export interface userLoginBody {
  /**
   * 验证码
   */
  captchaCode: string
  /**
   * 验证码id
   */
  captchaId: string
  /**
   * 密码
   */
  password: string
  /**
   * 用户名
   */
  username: string
}
