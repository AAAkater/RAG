import { fileURLToPath, URL } from "node:url"

import vue from "@vitejs/plugin-vue"
import { defineConfig } from "vite"

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    host: "127.0.0.1",
    port: 5173,
    proxy: {
      "/api/v1": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        rewrite: (path: string) => path.replace(/^\/api\/v1/, ""),
      },
      // "/m1/4426654-4071958-f6f7b997": {
      //   target: "http://127.0.0.1:4523",
      //   changeOrigin: true,
      //   rewrite: (path: string) =>
      //     path.replace(/^\/m1\/4426654-4071958-f6f7b997/, ""),
      // },
    },
  },
})
