import { type FormState } from "@/types"
import { defineStore } from "pinia"
import { ref } from "vue"
export const useUserStore = defineStore(
  "user",
  () => {
    const access_token = ref("")
    const refresh_token = ref<string>("")
    const password = ref("")
    const username = ref("")
    const is_remember = ref(false)
    const updateInfo = (newInfo: FormState) => {
      username.value = newInfo.username
      password.value = newInfo.password
      is_remember.value = newInfo.remember
    }
    const updateToken = (newAccessToken: string, newRefreshToken: string) => {
      access_token.value = newAccessToken
      refresh_token.value = newRefreshToken
    }
    const tokenExists = () => {
      return access_token.value !== "" && refresh_token.value !== ""
    }
    const removeToken = () => {
      access_token.value = ""
      refresh_token.value = ""
    }
    const removeUser = () => {
      localStorage.removeItem("user")
    }
    return {
      username,
      password,
      is_remember,
      access_token,
      refresh_token,
      updateInfo,
      updateToken,
      removeToken,
      tokenExists,
      removeUser,
    }
  },
  {
    persist: true,
  },
)
