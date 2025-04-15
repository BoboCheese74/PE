export const signinRules = {
  // 用户名验证规则
  username: [(v: string) => !!v || '用户名不能为空'],

  // 密码验证规则
  password: [(v: string) => !!v || '密码不能为空'],
}
