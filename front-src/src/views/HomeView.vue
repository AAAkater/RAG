<script setup lang="ts">
import MetaDisplay from '@/components/MetaDisplay.vue'
import { apiBase } from '@/constants'
import type { ContextItem } from '@/types'
import { CheckOutlined, ExclamationOutlined } from '@ant-design/icons-vue'
import type { NotificationPlacement } from 'ant-design-vue'
import { notification } from 'ant-design-vue'
import axios from 'axios'
import { h, nextTick, ref } from 'vue'
const openNotification = (placement: NotificationPlacement, desc: string, status: boolean) => {
  if (status)
    notification.open({
      message: `操作成功`,
      description: desc,
      placement,
      icon: () => h(CheckOutlined, { style: 'color: green' }),
      duration: 3
    })
  else
    notification.open({
      message: `请求错误！`,
      description: desc,
      placement,
      icon: () => h(ExclamationOutlined, { style: 'color: red' }),
      duration: 3
    })
}
const context = ref<ContextItem[]>([])

const input = ref('')
const isHover = ref(false)
const isLoading = ref(false)
const scrollRef = ref<HTMLDivElement | null>(null)
const uploadFile = ref<File | null>()

function readFile() {
  const inputFile = document.querySelector<HTMLInputElement>('#myFile')
  let file = inputFile?.files?.[0]
  uploadFile.value = file
}

async function handleUpload(type: string) {
  if (uploadFile.value) {
    if (
      (type === 'Document' && uploadFile.value.type !== 'application/pdf') ||
      (type === 'Video' && uploadFile.value.type !== 'video/mp4') ||
      (type === 'Image' && uploadFile.value.type !== 'image/png') ||
      (type === 'Audio' && uploadFile.value.type !== 'audio/wav')
    ) {
      openNotification('topRight', '请检查上传文件类型！', false)
      return
    }

    let formData = new FormData()
    formData.append('file', uploadFile.value)
    await axios
      .post(apiBase + '/upload' + type, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 5000
      })
      .then((response) => {
        console.log(response.data)
        openNotification('topRight', '上传成功！', true)
      })
      .catch((e) => {
        console.log(e)
        openNotification('topRight', '上传失败，请求错误！', false)
        return
      })
  }
}

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
          class="absolute w-auto h-auto bg-gray-200 rounded-lg bottom-[70px] flex flex-col justify-start items-start p-2 drop-shadow-xl"
        >
          <svg
            @click="(isHover = false), (uploadFile = null)"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="size-6 self-end cursor-pointer"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
          </svg>

          <input id="myFile" type="file" @change="readFile" placeholder="uploadFile?.name" />
          <button
            class="flex flex-row gap-2 items-center h-[50px] hover:text-gray-400"
            @click="handleUpload('Document')"
          >
            <svg
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
                d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"
              />
            </svg>

            上传PDF
          </button>
          <button
            class="flex flex-row gap-2 items-center h-[50px] hover:text-gray-400"
            @click="handleUpload('Image')"
          >
            <svg
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
                d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 0 0 1.5-1.5V6a1.5 1.5 0 0 0-1.5-1.5H3.75A1.5 1.5 0 0 0 2.25 6v12a1.5 1.5 0 0 0 1.5 1.5Zm10.5-11.25h.008v.008h-.008V8.25Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z"
              />
            </svg>

            上传图片
          </button>
          <button
            class="flex flex-row gap-2 items-center h-[50px] hover:text-gray-400"
            @click="handleUpload('Audio')"
          >
            <svg
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
                d="M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z"
              />
            </svg>

            上传音频
          </button>
          <button
            class="flex flex-row gap-2 items-center h-[50px] hover:text-gray-400"
            @click="handleUpload('Video')"
          >
            <svg
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
                d="m15.75 10.5 4.72-4.72a.75.75 0 0 1 1.28.53v11.38a.75.75 0 0 1-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 0 0 2.25-2.25v-9a2.25 2.25 0 0 0-2.25-2.25h-9A2.25 2.25 0 0 0 2.25 7.5v9a2.25 2.25 0 0 0 2.25 2.25Z"
              />
            </svg>

            上传视频
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
