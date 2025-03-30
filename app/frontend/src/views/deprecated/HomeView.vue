<script setup lang="ts">
import MetaDisplay from "@/components/MetaDisplay.vue"
import { apiBase } from "@/constants"
import type { ContextItem } from "@/types"
import openNotification from "@/utils/openNotification"

import axios from "axios"
import { nextTick, ref } from "vue"

const context = ref<ContextItem[]>([])

const input = ref("")
const isHover = ref(false)
const isLoading = ref(false)
const scrollRef = ref<HTMLDivElement | null>(null)
const uploadFile = ref<File | null>()

function readFile() {
  const inputFile = document.querySelector<HTMLInputElement>("#myFile")
  let file = inputFile?.files?.[0]
  uploadFile.value = file
  console.log(uploadFile.value)
}

async function handleUpload(type: string) {
  if (uploadFile.value) {
    if (
      (type === "Document" && uploadFile.value.type !== "application/pdf") ||
      (type === "Video" && uploadFile.value.type !== "video/mp4") ||
      (type === "Image" &&
        uploadFile.value.type !== "image/png" &&
        uploadFile.value.type !== "image/jpeg") ||
      (type === "Audio" && uploadFile.value.type !== "audio/wav")
    ) {
      openNotification("topRight", "请检查上传文件类型！", false)
      return
    }

    let formData = new FormData()
    formData.append("file", uploadFile.value)
    await axios
      .post(apiBase + "/upload" + type, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        timeout: 5000,
      })
      .then((response) => {
        console.log(response.data)
        openNotification("topRight", "上传成功！", true)
      })
      .catch((e) => {
        console.log(e)
        openNotification("topRight", "上传失败，请求错误！", false)
        return
      })
  }
}

async function handleSend() {
  if (input.value.trim() === "") {
    return
  }

  isLoading.value = true

  context.value.push({
    from: "user",
    data: input.value,
  })

  nextTick(() =>
    scrollRef.value?.scrollTo({
      top: scrollRef.value?.scrollHeight,
      behavior: "smooth",
    }),
  )
  const resp = await axios
    .get(apiBase + "/query", { timeout: 5000, params: { desc: input.value } })
    .then((response) => response.data)
    .catch((error: any) => {
      console.log(error.code)
      isLoading.value = false

      if (error.code == "ECONNABORTED") {
        context.value.push({
          from: "assistant",
          data: "请求超时，请检测当前网络环境。",
          metadata: [],
          success: false,
          inquiryContent: input.value,
        })
      } else {
        context.value.push({
          from: "assistant",
          data: "请求错误，请联系工作人员。",
          metadata: [],
          success: false,
          inquiryContent: input.value,
        })
      }
      input.value = ""

      return
    })
  context.value.push({
    from: "assistant",
    data: resp.data.answer,
    metadata: resp.data.metadata,
    success: true,
  })

  isLoading.value = false
  input.value = ""
  console.log(context.value)

  nextTick(() =>
    scrollRef.value?.scrollTo({
      top: scrollRef.value?.scrollHeight,
      behavior: "smooth",
    }),
  )
}

async function handleClear() {
  await axios.post(apiBase + "/clear")
  context.value = []
}
</script>

<template>
  <main
    class="mx-auto flex h-[100vh] max-w-screen-md flex-col items-center border-x bg-white"
  >
    <div
      v-if="context.length === 0"
      class="flex flex-grow flex-col items-center justify-center gap-8"
    >
      <div
        class="flex h-20 w-20 items-center justify-center rounded-full border"
      >
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
          <path
            d="m8 18-4 4V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2Z"
          />
          <path d="M2 12h2" />
          <path d="M9 11v2" />
          <path d="M15 11v2" />
          <path d="M20 12h2" />
        </svg>
      </div>
      <span class="text-2xl">基于langchain的多模态知识库检索系统</span>
      <div class="flex flex-col items-center gap-3">
        <span class="text-lg">想要检索些什么</span>
        <ul class="list-disc space-y-2 pl-5 text-gray-500">
          <li class="text-xs">
            资源检索：在查找栏输入您要查找的关键字，然后单击“发送”按钮。
          </li>
          <li class="text-xs">
            下载资源：在搜索结果中，您可以通过点击“下载”按钮将所需资源.
          </li>
          <li class="text-xs">
            错误处理：如果搜索请求未能成功执行，系统会显示错误信息。
          </li>
          <li class="text-xs">
            资源上传：您可以上传所需文件类型以扩大我们的数据库。
          </li>
          <li class="text-xs">
            消息清理：您可以通过点击右侧垃圾箱图标清空所有消息记录。
          </li>
        </ul>
      </div>
    </div>

    <div
      v-else
      class="relative flex w-full flex-grow flex-col"
    >
      <div
        class="absolute inset-0 overflow-auto"
        ref="scrollRef"
      >
        <div
          v-for="(item, index) in context"
          :key="index + item.from + item.data"
          class="flex gap-2 border-b p-4"
          :class="{ 'flex-row-reverse': item.from !== 'assistant' }"
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
            class="flex-shrink-0 opacity-75"
          >
            <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
            <circle
              cx="12"
              cy="7"
              r="4"
            />
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
            class="flex-shrink-0 opacity-75"
          >
            <path d="M12 6V2H8" />
            <path
              d="m8 18-4 4V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2Z"
            />
            <path d="M2 12h2" />
            <path d="M9 11v2" />
            <path d="M15 11v2" />
            <path d="M20 12h2" />
          </svg>
          <div class="flex flex-grow flex-col">
            <div
              v-if="item.from === 'assistant'"
              class="self-start"
            >
              <div class="h-5 text-sm leading-5 opacity-75">
                Multimodality RAG
              </div>
              <div class="mt-2 rounded-lg bg-blue-600 p-2 text-white">
                {{ item.data }}
              </div>
              <div
                v-if="!item.success"
                class="h-5 w-auto text-sm leading-5 hover:opacity-30"
              >
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
                class="mt-2 flex flex-row flex-wrap gap-2 rounded-lg border p-2"
              >
                <div
                  v-for="_item in item.metadata.sort((a, b) =>
                    a.type.localeCompare(b.type),
                  )"
                  :key="_item.id"
                  :class="{ 'w-full': _item.type !== 'image' }"
                >
                  <MetaDisplay
                    :type="_item.type"
                    :filename="_item.filename"
                    :id="_item.id"
                  />
                </div>
              </div>
            </div>
            <div
              v-else
              class="self-end"
            >
              <div
                class="h-5 text-sm leading-5 opacity-75"
                style="direction: rtl"
              >
                你
              </div>
              <div class="mt-2 rounded-lg bg-gray-200 p-2">{{ item.data }}</div>
            </div>
          </div>
        </div>

        <div
          v-if="isLoading"
          class="flex gap-2 border-b p-4"
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
            class="flex-shrink-0 opacity-75"
          >
            <path d="M12 6V2H8" />
            <path
              d="m8 18-4 4V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2Z"
            />
            <path d="M2 12h2" />
            <path d="M9 11v2" />
            <path d="M15 11v2" />
            <path d="M20 12h2" />
          </svg>
          <div class="flex flex-grow flex-col">
            <div>
              <div class="h-5 text-sm leading-5 opacity-75">Image RAG</div>
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

    <div class="flex w-full items-center gap-2 p-4">
      <div class="w-auto">
        <div
          v-if="isHover"
          class="absolute bottom-[70px] flex h-auto w-auto flex-col items-start justify-start rounded-lg bg-gray-200 p-2 drop-shadow-xl"
        >
          <svg
            @click="(isHover = false), (uploadFile = null)"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="size-6 cursor-pointer self-end"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M6 18 18 6M6 6l12 12"
            />
          </svg>

          <input
            id="myFile"
            type="file"
            accept=".jpg, .png, .pdf, .mp3, .mp4"
            @change="readFile"
            placeholder="uploadFile?.name"
          />
          <button
            class="flex h-[50px] flex-row items-center gap-2 hover:text-gray-400"
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
            class="flex h-[50px] flex-row items-center gap-2 hover:text-gray-400"
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
            class="flex h-[50px] flex-row items-center gap-2 hover:text-gray-400"
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
            class="flex h-[50px] flex-row items-center gap-2 hover:text-gray-400"
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
          class="rounded-lg bg-gray-900 p-2 text-white hover:opacity-75"
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
            <line
              x1="12"
              y1="3"
              x2="12"
              y2="15"
            />
          </svg>
        </div>
      </div>
      <div class="relative flex-grow">
        <input
          class="h-12 w-full rounded-lg border px-3 text-lg shadow-sm outline-none disabled:text-gray-600"
          type="text"
          placeholder="输入检索内容……"
          v-model="input"
          :disabled="isLoading"
        />
        <button
          class="absolute right-2 top-2 flex h-8 w-8 items-center justify-center rounded-lg bg-gray-900 text-white shadow-sm hover:opacity-75 disabled:opacity-50"
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
        class="flex h-10 w-10 items-center justify-center rounded-full text-gray-600 hover:bg-gray-950/5"
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
          <line
            x1="10"
            x2="10"
            y1="11"
            y2="17"
          />
          <line
            x1="14"
            x2="14"
            y1="11"
            y2="17"
          />
        </svg>
      </button>
    </div>
  </main>
</template>

<style scoped></style>
