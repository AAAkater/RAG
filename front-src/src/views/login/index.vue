<script setup lang="ts">
import LoginLogo from "./components/LoginLogo.vue"
import LoginForm from "./components/LoginForm.vue"
import RegisterForm from "./components/RegisterForm.vue"
import { computed, ref } from "vue"
import { useRoute } from "vue-router"
const route = useRoute()
const isLogin = ref(computed(() => route.path === "/login"))
</script>

<template>
  <div
    :class="[
      'h-screen w-full',
      'flex items-center justify-center',
      'bg-gradient-to-r from-[#74ebd5] to-[#9face6]',
    ]"
  >
    <div :class="['h-1/2 w-1/2 min-w-80', 'flex shadow-2xl']">
      <LoginLogo />
      <div
        class="flex h-full w-1/2 items-center justify-center outline max-sm:w-full"
      >
        <LoginForm v-if="isLogin" />
        <RegisterForm v-else />
      </div>
    </div>
  </div>
</template>

<style scoped></style>
