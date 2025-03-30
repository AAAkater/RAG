import { defineStore } from "pinia"
import { ref } from "vue"

export const useCaptchaStore = defineStore("captcha", () => {
  const captchaId = ref("")
  const updateCaptcha = (newCaptchaId: string) => {
    captchaId.value = newCaptchaId
  }

  return {
    updateCaptcha,
  }
})
