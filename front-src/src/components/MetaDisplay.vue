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
      console.log(e)
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
  <h5>{{ filename }}</h5>
  <div v-if="type == `image`">
    <div
      style="position: relative; width: 100%; height: 100%"
      class="text-transparent hover:text-slate-950"
      @click="downloadFile('/getImage?id=b_aea1b74356186eb76b54a64359eed5d0', 'png')"
    >
      <svg
        style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%)"
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
        :src="apiBase + `/getImage?id=b_aea1b74356186eb76b54a64359eed5d0`"
        class="w-[120px] aspect-square object-cover rounded-md hover:opacity-50"
      />
    </div>
  </div>
  <div v-else-if="type == `pdf`">
    <iframe :src="apiBase + `/getDocument?id=第五次作业答案`" width="100%" height="100%">
      This browser does not support PDFs. Please download the PDF to view it:
      <a href="/index.pdf">Download PDF</a>
    </iframe>
    <a @click="downloadFile(`/getDocument?id=第五次作业答案`, 'pdf')">{{
      apiBase + `/getDocument?id=第五次作业答案`
    }}</a>
  </div>
</template>
