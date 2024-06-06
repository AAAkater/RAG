<script setup lang="ts">
import { apiBase } from '@/constants'
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
    class="border-gray-900 rounded-md p-2 flex flex-row justify-between flex-wrap gap-2 border-2"
  >
    <span v-if="type !== `image`">{{ filename }}</span>
    <div
      v-if="type == `image`"
      style="position: relative; width: 100%; height: 100%"
      class="text-transparent hover:text-slate-950 w-auto"
      @click="downloadFile('/getImage?id=' + id, 'png')"
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
        :src="apiBase + `/getImage?id=` + id"
        class="w-[120px] aspect-square object-cover rounded-md hover:opacity-50 cursor-pointer"
      />
    </div>
    <div v-else-if="type == `pdf`" class="justify-self-end">
      <a
        class="hover:text-gray-500 text-sm underline underline-offset-4 decoration-1 cursor-pointer"
        :href="apiBase + `/getDocument?id=` + id"
        target="_blank"
        >{{ apiBase + `/getDocument?id=` + id }}</a
      >
    </div>
    <div v-else-if="type == `mp3`" class="justify-self-end">
      <a
        class="hover:text-gray-500 text-sm underline underline-offset-4 decoration-1 cursor-pointer"
        :href="apiBase + `/getAudio?id=` + id"
        target="_blank"
        >{{ apiBase + `/getAudio?id=` + id }}</a
      >
    </div>
    <div v-else-if="type == `mp4`">
      <a
        class="hover:text-gray-500 text-sm underline underline-offset-4 decoration-1 cursor-pointer"
        :href="apiBase + `//getVideo?id=` + id"
        target="_blank"
        >{{ apiBase + `//getVideo?id=` + id }}</a
      >
    </div>
  </div>
</template>
