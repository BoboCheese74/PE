import { $http } from ".";

export const loginApi = (data: { username: string; password: string }) => {
    return $http({
        method: 'POST',
        url: '/user/login/',
        data,
    })
}