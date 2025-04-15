export const paperRules = {
  // 关键词验证规则
  keywords: [(v: string) => !!v || '关键词不能为空'],

  // 提纲验证规则
  outline: [(v: string) => !!v || '提纲不能为空'],
}
