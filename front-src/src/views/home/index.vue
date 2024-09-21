<script setup lang="ts">
import {
  RightOutlined,
  GithubOutlined,
  UserOutlined,
} from "@ant-design/icons-vue"
import { ref, h } from "vue"
import type { MenuTheme } from "ant-design-vue"
import { Menu, Layout, Button, Switch, Avatar } from "ant-design-vue"
import { useRouter } from "vue-router"
const theme = ref<MenuTheme>("light")
const changeTheme = (checked: boolean | string | number) => {
  theme.value = checked ? "dark" : "light"
}
const selectedKeys = ref<string[]>(["2"])

const router = useRouter()

const startOnclick = () => {
  router.push("/dashboard")
}
</script>

<template>
  <div class="flex h-screen flex-col">
    <Layout.Header class="">
      <Menu
        v-model:selectedKeys="selectedKeys"
        :theme="theme"
        mode="horizontal"
        :style="{ lineHeight: '64px' }"
        class="flex justify-end"
      >
        <Menu.Item key="1">nav 1</Menu.Item>
        <Menu.Item key="2">nav 2</Menu.Item>
        <Menu.Item key="3">nav 3</Menu.Item>
        <Menu.Item key="4">
          <Switch
            :checked="theme === 'dark'"
            checked-children="Dark"
            un-checked-children="Light"
            @change="changeTheme"
          />
        </Menu.Item>
        <Menu.Item key="5">
          <GithubOutlined />
        </Menu.Item>
        <Menu.Item>
          <Avatar>
            <template #icon>
              <UserOutlined />
            </template>
          </Avatar>
        </Menu.Item>
      </Menu>
    </Layout.Header>
    <Layout.Content :class="['flex items-center justify-center', 'flex-grow']">
      <div class="">
        <div class="mb-6 font-mono text-6xl">多模态知识图谱RAG</div>
        <div class="flex justify-center">
          <Button
            type="primary"
            :icon="h(RightOutlined)"
            size="large"
            shape="round"
            @click="startOnclick"
          >
            快速上手
          </Button>
        </div>
      </div>
    </Layout.Content>
  </div>
</template>

<style scoped></style>
