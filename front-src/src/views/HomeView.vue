<script setup lang="ts">
import MetaDisplay from '@/components/MetaDisplay.vue'
import { apiBase } from '@/constants'
import type { ContextItem } from '@/types'
import axios from 'axios'
import { nextTick, ref } from 'vue'
const context = ref<ContextItem[]>([])

const input = ref('')
const isHover = ref(false)
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
  const resp = await axios
    .get(apiBase + '/query', { timeout: 5000, params: { desc: input.value } })
    .then((response) => response.data)
    .catch((error: any) => {
      console.log(error.code)
      isLoading.value = false

      if (error.code == 'ECONNABORTED') {
        context.value.push({
          from: 'assistant',
          data: '请求超时，请检测当前网络环境。',
          metadata: [],
          success: false,
          inquiryContent: input.value
        })
      } else {
        context.value.push({
          from: 'assistant',
          data: '请求错误，请联系工作人员。',
          metadata: [],
          success: false,
          inquiryContent: input.value
        })
      }
      input.value = ''

      return
    })
  context.value.push({
    from: 'assistant',
    data: resp.data.answer,
    metadata: resp.data.metadata,
    success: true
  })

  isLoading.value = false
  input.value = ''
  console.log(context.value)

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
            v-if="item.from === 'user'"
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
          <svg
            v-else
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
            <path d="M12 6V2H8" />
            <path d="m8 18-4 4V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2Z" />
            <path d="M2 12h2" />
            <path d="M9 11v2" />
            <path d="M15 11v2" />
            <path d="M20 12h2" />
          </svg>
          <div class="flex flex-grow flex-col">
            <div v-if="item.from === 'assistant'">
              <div class="text-sm h-5 leading-5 opacity-75">Multimodality RAG</div>
              <div class="mt-2">{{ item.data }}</div>
              <div v-if="!item.success" class="text-sm h-5 leading-5 hover:opacity-30 w-auto">
                <svg
                  @click="
                    () => {
                      input = item.inquiryContent || ''
                      handleSend()
                    }
                  "
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="size-6"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M19.5 12c0-1.232-.046-2.453-.138-3.662a4.006 4.006 0 0 0-3.7-3.7 48.678 48.678 0 0 0-7.324 0 4.006 4.006 0 0 0-3.7 3.7c-.017.22-.032.441-.046.662M19.5 12l3-3m-3 3-3-3m-12 3c0 1.232.046 2.453.138 3.662a4.006 4.006 0 0 0 3.7 3.7 48.656 48.656 0 0 0 7.324 0 4.006 4.006 0 0 0 3.7-3.7c.017-.22.032-.441.046-.662M4.5 12l3 3m-3-3-3 3"
                  />
                </svg>
              </div>
              <div
                v-if="item && item.metadata && item.metadata.length !== 0"
                class="mt-2 border rounded-lg p-2 flex flex-col gap-2 flex-wrap"
              >
                <div
                  v-for="_item in item.metadata.sort((a, b) => a.type.localeCompare(b.type))"
                  :key="_item.id"
                >
                  <MetaDisplay :type="_item.type" :filename="_item.filename" :id="_item.id" />
                </div>
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
            <path d="M12 6V2H8" />
            <path d="m8 18-4 4V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2Z" />
            <path d="M2 12h2" />
            <path d="M9 11v2" />
            <path d="M15 11v2" />
            <path d="M20 12h2" />
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
      <div class="w-auto">
        <div
          v-if="isHover"
          @mouseleave="isHover = false"
          class="absolute w-auto h-[100px] bg-gray-200 rounded-lg bottom-[70px] flex flex-col justify-start items-start p-2 drop-shadow-xl"
        >
          <button class="flex flex-row gap-2 items-center h-[50px] hover:text-gray-400">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="feather feather-file"
            >
              <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path>
              <polyline points="13 2 13 9 20 9"></polyline>
            </svg>
            上传文档
          </button>
          <button class="flex flex-row gap-2 items-center h-[50px] hover:text-gray-400">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="feather feather-image"
            >
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
              <circle cx="8.5" cy="8.5" r="1.5"></circle>
              <polyline points="21 15 16 10 5 21"></polyline>
            </svg>
            上传图片
          </button>
        </div>
        <div
          @mouseover="isHover = true"
          class="bg-gray-900 p-2 rounded-lg text-white hover:opacity-75"
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
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="17 8 12 3 7 8" />
            <line x1="12" y1="3" x2="12" y2="15" />
          </svg>
        </div>
      </div>
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
