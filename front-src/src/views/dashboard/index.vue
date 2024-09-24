<script lang="ts" setup>
import { ref, h } from "vue"
import {
  MenuUnfoldOutlined,
  MenuFoldOutlined,
  AppstoreOutlined,
  CommentOutlined,
  HomeOutlined,
} from "@ant-design/icons-vue"
import MenuLogo from "./components/MenuLogo.vue"
import { Layout, Menu } from "ant-design-vue"
import { useRouter } from "vue-router"
const selectedKeys = ref<string[]>(["home"])
const collapsed = ref<boolean>(false)
const router = useRouter()
const items = ref([
  {
    key: "home",
    icon: () => h(HomeOutlined),
    label: "首页",
    title: "回到起点",
    click: () => {
      router.push("/dashboard/home")
    },
  },
  {
    key: "base",
    icon: () => h(AppstoreOutlined),
    label: "知识库",
    title: "管理你的私人知识库",
    click: () => {
      router.push("/dashboard/knowledge-base")
    },
  },
  {
    key: "dialog",
    icon: () => h(CommentOutlined),
    label: "对话",
    title: "在这里查看所有会话记录",
    click: () => {
      router.push("/dashboard/dialog")
    },
  },
])
</script>

<template>
  <Layout>
    <Layout.Sider
      v-model:collapsed="collapsed"
      :trigger="null"
      collapsible
      class="h-screen"
    >
      <MenuLogo :collapsed="collapsed" />
      <Menu
        v-model:selectedKeys="selectedKeys"
        theme="dark"
        mode="inline"
      >
        <Menu.Item
          v-for="item of items"
          :key="item.key"
          :icon="item.icon"
          :title="item.title"
          @click="item.click"
        >
          {{ item.label }}
        </Menu.Item>
      </Menu>
    </Layout.Sider>
    <Layout>
      <Layout.Header style="background: #fff">
        <MenuUnfoldOutlined
          v-if="collapsed"
          @click="() => (collapsed = !collapsed)"
        />
        <MenuFoldOutlined
          v-else
          @click="() => (collapsed = !collapsed)"
        />
      </Layout.Header>
      <Layout.Content>
        <RouterView />
      </Layout.Content>
    </Layout>
  </Layout>
</template>

<style scoped></style>
