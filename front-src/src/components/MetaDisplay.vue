<script setup lang="ts">
import { apiBase } from '@/constants'
import openNotification from '@/util/openNotification'
import axios from 'axios'

const downloadFile = async (url: string, type: string) => {
  await axios
    .get(apiBase + url, {
      responseType: 'blob',
      withCredentials: false
    })
    .then((e) => {
      const href = URL.createObjectURL(e.data)
      const aLink = document.createElement('a')
      aLink.style.display = 'none'
      aLink.href = href
      aLink.download = `图片.${type}`
      aLink.click()
      URL.revokeObjectURL(apiBase + url)
      openNotification('topRight', '下载成功', true)
    })
    .catch((e) => {
      console.log(e)
      openNotification('topRight', e.message, false)
    })
}

const { filename, id, type } = defineProps({
  filename: String,
  id: String,
  type: String
})
</script>

<template>
  <div
    v-if="type == `image`"
    style="position: relative; width: 120px; height: 100%"
    class="text-transparent hover:text-slate-950"
  >
    <svg
      style="position: absolute; top: 50%; left: 60px; transform: translate(-50%, -50%)"
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="1.5"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="7 10 12 15 17 10" />
      <line x1="12" y1="15" x2="12" y2="3" />
    </svg>
    <img
      @click="downloadFile('/getImage?id=' + id, 'png')"
      :src="apiBase + `/getImage?id=` + id"
      class="w-[120px] aspect-square object-cover rounded-md hover:opacity-50 cursor-pointer"
    />
  </div>

  <div
    v-else
    class="rounded-md p-2 flex flex-row justify-between flex-wrap gap-2"
    style="border: 1px solid gray"
  >
    <span class="text-zinc-700 font-medium">{{ filename }}</span>
    <div v-if="type == `pdf`" class="justify-self-end">
      <a
        class="hover:text-gray-400 text-xs cursor-pointer text-zinc-700"
        :href="apiBase + `/getDocument?id=` + id"
        target="_blank"
        >下载</a
      >
    </div>
    <div v-else-if="type == `mp3`" class="justify-self-end">
      <a
        class="hover:text-gray-400 text-xs cursor-pointer text-zinc-700"
        :href="apiBase + `/getAudio?id=` + id"
        target="_blank"
        >下载</a
      >
    </div>
    <div v-else-if="type == `mp4`" class="justify-self-end">
      <a
        class="hover:text-gray-400 text-xs cursor-pointer text-zinc-700"
        :href="apiBase + `//getVideo?id=` + id"
        target="_blank"
        >下载</a
      >
    </div>
  </div>
</template>
