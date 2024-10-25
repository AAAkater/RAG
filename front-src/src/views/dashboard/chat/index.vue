<script setup lang="ts">
import { Textarea } from "ant-design-vue"
import { ref } from "vue"

const value1 = ref("")
</script>

<template>
  <div :class="['relative w-full']">
    <div :class="['h-[90vh] w-full', 'scrollbar-hide overflow-auto']">
      <div class="flex h-[2000px] w-full items-center justify-center">chat</div>
    </div>
    <Textarea
      :class="[
        'absolute bottom-1 left-1/2 -translate-x-1/2',
        'w-4/5 min-w-[200px] max-w-[300px]',
      ]"
      v-model:value="value1"
      placeholder="请输入你想要的问的"
      :auto-size="{ minRows: 2, maxRows: 5 }"
    />
  </div>
</template>

<style lang="css" scoped></style>
