import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'
import { createApp } from 'vue'
import App from './App.vue'
import './main.css'
import router from './router'

const app = createApp(App)

app.use(router)

app.use(Antd).mount('#app')
