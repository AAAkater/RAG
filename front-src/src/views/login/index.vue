<script setup lang="ts">
import Left from "./components/LoginLogo.vue"
import Right from "./components/LoginForm.vue"
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
      <Left />
      <Right />
    </div>
  </div>
</template>

<style scoped></style>
