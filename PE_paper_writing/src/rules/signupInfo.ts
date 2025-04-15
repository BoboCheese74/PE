export const signupRules = {
  // 用户名验证规则
  username: [
    (v: string) => !!v || '用户名不能为空',
    (v: string) => v.length >= 3 || '用户名长度不能小于3个字符',
    (v: string) => v.length <= 20 || '用户名长度不能超过20个字符',
    (v: string) => /^[a-zA-Z0-9_]+$/.test(v) || '用户名只能包含字母、数字和下划线',
  ],

  // 密码验证规则
  password: [
    (v: string) => !!v || '密码不能为空',
    (v: string) => v.length >= 8 || '密码长度不能小于8个字符',
    (v: string) => v.length <= 30 || '密码长度不能超过30个字符',
    (v: string) => /[A-Z]/.test(v) || '密码必须包含至少一个大写字母',
    (v: string) => /[a-z]/.test(v) || '密码必须包含至少一个小写字母',
    (v: string) => /\d/.test(v) || '密码必须包含至少一个数字',
  ],

  // 邀请码验证规则
  invitationCode: [
    (v: string) => !!v || '邀请码不能为空',
    (v: string) => v.length === 8 || '邀请码长度必须为8位',
    (v: string) => /^[A-Za-z0-9]{8}$/.test(v) || '邀请码格式不正确',
  ],
}
