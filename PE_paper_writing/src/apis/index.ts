import router from '@/router'
import axios, { AxiosError, type AxiosRequestConfig } from 'axios'
import { useSnackbar } from '@/plugins/snackbar.ts'
import { useUserInfoStore } from '@/stores/userinfo.store'

export const httpInstance = axios.create()

export type bkResponse = {
  data: unknown
  code: number
  message: string
  succeed: boolean
}

//设置请求根路径
httpInstance.defaults.baseURL = import.meta.env.VITE_API_URL

//响应拦截器
export const $http = async (config: AxiosRequestConfig) => {
  const snackbar = useSnackbar() // 获取snackbar实例
  const userInfoStore = useUserInfoStore()

  try {
    const axiosResponse = await httpInstance<bkResponse>(config)
    const bkResponse = axiosResponse.data
    if (!bkResponse?.succeed) {
      let errTitle: string = 'Error'
      switch (bkResponse.code) {
        case 400:
          errTitle = 'Bad Request'
          userInfoStore.removeAuth()
          snackbar.show({ text: '如果用户被标记为禁用状态', color: 'error' })
          router.push('/login')
          break
        case 401:
          errTitle = 'Unauthorized'
          userInfoStore.removeAuth()
          snackbar.show({ text: '未授权', color: 'error' })
          router.push('/login')
          break
        case 403:
          errTitle = 'Forbidden'
          break
        case 4001:
          errTitle = 'JWTerror'
          snackbar.show({ text: '未授权', color: 'error' })
          localStorage.removeItem('token')
          router.push('/login')
          break
        case 2001:
          errTitle = '2001Error'
          snackbar.show({ text: '用户名或密码错误', color: 'error' })
          break
        case 500:
          errTitle = 'ServerError'
          break
        default:
          errTitle = 'Unknown'
      }
      const err = new Error(bkResponse?.message || 'Unknown')
      err.name = errTitle
      throw err
    }
    return bkResponse
  } catch (err) {
    if (err instanceof AxiosError) {
      snackbar.show({ text: '网络错误', color: 'error' })
    }
    throw err
  }
}
