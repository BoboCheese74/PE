import { $http } from '.'

export const loginApi = (data: FormData) => {
  return $http({
    method: 'POST',
    url: '/token',
    data,
  })
}
