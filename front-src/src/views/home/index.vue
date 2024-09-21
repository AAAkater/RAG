<script setup lang="ts">
import {
  RightOutlined,
  GithubOutlined,
  UserOutlined,
} from "@ant-design/icons-vue"
import { ref, h } from "vue"
import { Menu, Layout, Button, Avatar } from "ant-design-vue"
import { useRouter } from "vue-router"
const selectedKeys = ref<string[]>([""])

const router = useRouter()

const startOnclick = () => {
  router.push("/dashboard")
}
</script>

<template>
  <Layout class="h-screen">
    <Layout.Header
      class="flex"
      style="padding: 0"
    >
      <div class="ml-4 p-2">
        <img
          src="@/assets/icons/logo.svg"
          alt=""
          class="h-full w-auto"
        />
      </div>
      <Menu
        v-model:selectedKeys="selectedKeys"
        theme="dark"
        mode="horizontal"
        :style="{ lineHeight: '64px' }"
        class="mx-0 flex w-full justify-end"
      >
        <Menu.Item key="1">nav 1</Menu.Item>
        <Menu.Item key="2">nav 2</Menu.Item>
        <Menu.Item key="3">nav 3</Menu.Item>
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
    <Layout.Content class="flex h-full items-center justify-center outline">
      <div class="flex h-[400px]">
        <img
          src="@/assets/icons/logo.svg"
          alt=""
          class="h-full w-auto"
        />
        <div class="flex items-center justify-center px-20">
          <div>
            <div class="mb-16 font-mono text-6xl">多模态知识图谱RAG</div>
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
        </div>
      </div>
    </Layout.Content>
  </Layout>
</template>

<style scoped></style>
