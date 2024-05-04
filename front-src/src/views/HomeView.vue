<script setup lang="ts">
import { apiBase } from '@/constants'
import type { ContextItem } from '@/types'
import axios from 'axios'
import { nextTick, ref } from 'vue'

const context = ref<ContextItem[]>([])

const input = ref('')
const isLoading = ref(false)
const scrollRef = ref<HTMLDivElement | null>(null)

async function handleSend() {
  if (input.value.trim() === '') {
    return
  }

  isLoading.value = true

  context.value.push({
    from: 'user',
    data: input.value
  })

  nextTick(() =>
    scrollRef.value?.scrollTo({ top: scrollRef.value?.scrollHeight, behavior: 'smooth' })
  )

  const resp = await axios.get(apiBase + '/query', { params: { desc: input.value } })
  context.value.push({
    from: 'assistant',
    data: resp.data.answer,
    imageIds: resp.data.ids
  })

  isLoading.value = false
  input.value = ''

  nextTick(() =>
    scrollRef.value?.scrollTo({ top: scrollRef.value?.scrollHeight, behavior: 'smooth' })
  )
}

async function handleClear() {
  await axios.post(apiBase + '/clear')
  context.value = []
}
</script>

<template>
  <main class="bg-white border-x max-w-screen-md mx-auto h-[100vh] flex flex-col items-center">
    <div
      v-if="context.length === 0"
      class="flex flex-col items-center justify-center gap-8 flex-grow"
    >
      <div class="rounded-full border w-20 h-20 flex items-center justify-center">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="42"
          height="42"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M12 6V2H8" />
          <path d="m8 18-4 4V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2Z" />
          <path d="M2 12h2" />
          <path d="M9 11v2" />
          <path d="M15 11v2" />
          <path d="M20 12h2" />
        </svg>
      </div>
      <div class="text-xl">想要检索些什么</div>
    </div>

    <div v-else class="flex flex-col flex-grow relative w-full">
      <div class="absolute inset-0 overflow-auto" ref="scrollRef">
        <div
          v-for="(item, index) in context"
          :key="index + item.from + item.data"
          class="p-4 flex gap-2 border-b"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="opacity-75 flex-shrink-0"
          >
            <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
          <div class="flex flex-grow flex-col">
            <div v-if="item.from === 'assistant'">
              <div class="text-sm h-5 leading-5 opacity-75">Image RAG</div>
              <div class="mt-2">{{ item.data }}</div>
              <div
                v-if="item.imageIds.length !== 0"
                class="mt-2 border rounded-lg p-2 flex gap-2 flex-wrap"
              >
                <img
                  v-for="id in item.imageIds"
                  :key="id"
                  :src="apiBase + '/image?id=' + id"
                  class="w-[120px] aspect-square object-cover rounded-md"
                />
              </div>
            </div>
            <div v-else>
              <div class="text-sm h-5 leading-5 opacity-75">你</div>
              <div class="mt-2">{{ item.data }}</div>
            </div>
          </div>
        </div>

        <div v-if="isLoading" class="p-4 flex gap-2 border-b">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="opacity-75 flex-shrink-0"
          >
            <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
          <div class="flex flex-grow flex-col">
            <div>
              <div class="text-sm h-5 leading-5 opacity-75">Image RAG</div>
              <div class="mt-2 flex gap-2 opacity-50">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  class="animate-spin"
                >
                  <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                </svg>
                推理中
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="w-full p-4 flex gap-2 items-center">
      <div class="flex-grow relative">
        <input
          class="w-full border rounded-lg shadow-sm text-lg px-3 h-12 outline-none disabled:text-gray-600"
          type="text"
          placeholder="输入检索内容……"
          v-model="input"
          :disabled="isLoading"
        />
        <button
          class="w-8 h-8 rounded-lg bg-gray-900 shadow-sm top-2 right-2 absolute text-white flex items-center justify-center hover:opacity-75 disabled:opacity-50"
          @click="handleSend"
          :disabled="isLoading"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="m3 3 3 9-3 9 19-9Z" />
            <path d="M6 12h16" />
          </svg>
        </button>
      </div>
      <button
        class="text-gray-600 w-10 h-10 flex items-center justify-center hover:bg-gray-950/5 rounded-full"
        @click="handleClear"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M3 6h18" />
          <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
          <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
          <line x1="10" x2="10" y1="11" y2="17" />
          <line x1="14" x2="14" y1="11" y2="17" />
        </svg>
      </button>
    </div>
  </main>
</template>

<style scoped></style>
