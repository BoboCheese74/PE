import { httpInstance } from "@/apis";
import router from "@/router";
import { defineStore } from "pinia";

export const useUserInfoStore = defineStore("userinfo-store", () => {
    const setAuth = (token: string, user: string) => {
        httpInstance.defaults.headers.common.Authorization = token;
        localStorage.setItem("currentUser", user);
        localStorage.setItem("token", token);
    };
    const authFormLocal = () => {
        const token = localStorage.getItem("token");
        const currentUser = localStorage.getItem("currentUser");
        if (token && currentUser) {
            setAuth(token, currentUser);
            return true;
        }
        return false;
    };
    const removeAuth = () => {
        delete httpInstance.defaults.headers.common.Authorization;
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        router.push("/login");
    };
    return {
        setAuth,
        authFormLocal,
        removeAuth,
    }
})