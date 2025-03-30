<script lang="ts" setup>
const props = defineProps({
  collapsed: {
    default: false,
    required: true,
    type: Boolean,
  },
})
</script>

<template>
  <div class="my-2 flex justify-evenly">
    <img
      src="@/assets/icons/logo.svg"
      alt=""
      class="h-10 w-auto"
    />
    <div
      v-if="!props.collapsed"
      class="flex items-center font-mono text-3xl text-white"
    >
      RAG
    </div>
  </div>
</template>

<style scoped></style>
