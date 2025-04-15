import router from '@/router'
import axios, { AxiosError, type AxiosRequestConfig } from 'axios'
import { useLoadingStore } from '@/stores/loading.ts'
import { useSnackbar } from '@/plugins/snackbar.ts'

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
  const loading = useLoadingStore()
  const snackbar = useSnackbar() // 获取snackbar实例

  loading.start() // 开始加载

  try {
    const axiosResponse = await httpInstance<bkResponse>(config)
    const bkResponse = axiosResponse.data
    if (!bkResponse?.succeed) {
      let errTitle: string = 'Error'
      switch (bkResponse.code) {
        case 401:
          errTitle = 'Unauthorized'
          snackbar.show({ text: '未授权', color: 'error' })
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
  } finally {
    loading.end() // 结束加载
  }
}
