import { type FormState } from "@/types"
import { defineStore } from "pinia"
import { ref } from "vue"
export const useUserStore = defineStore(
  "user",
  () => {
    const token = ref("")
    const password = ref("")
    const username = ref("")
    const remember = ref(false)
    const updateInfo = (newInfo: FormState) => {
      username.value = newInfo.username
      password.value = newInfo.password
      remember.value = newInfo.remember
    }
    const updateToken = (newToken: string) => {
      token.value = newToken
    }
    const removeUser = () => {
      localStorage.removeItem("user")
    }
    return {
      username,
      password,
      remember,
      token,
      updateInfo,
      updateToken,
      removeUser,
    }
  },
  {
    persist: true,
  },
)
