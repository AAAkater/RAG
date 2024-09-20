import Antd from "ant-design-vue"
import "ant-design-vue/dist/reset.css"
import { createApp } from "vue"
import App from "./App.vue"
import "./main.css"
import router from "./router"
import pinia from "./stores"

const app = createApp(App)
app.use(Antd)
app.use(pinia)
app.use(router)

app.mount("#app")
