<script lang="ts" setup>
import { ref } from "vue"
import {
  UserOutlined,
  VideoCameraOutlined,
  UploadOutlined,
  MenuUnfoldOutlined,
  MenuFoldOutlined,
} from "@ant-design/icons-vue"
import MenuLogo from "./components/MenuLogo.vue"
import { Layout, Menu } from "ant-design-vue"
const selectedKeys = ref<string[]>(["1"])
const collapsed = ref<boolean>(false)
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
        <Menu.Item key="1">
          <user-outlined />
          <span>nav 1</span>
        </Menu.Item>
        <Menu.Item key="2">
          <video-camera-outlined />
          <span>nav 2</span>
        </Menu.Item>
        <Menu.Item key="3">
          <upload-outlined />
          <span>nav 3</span>
        </Menu.Item>
      </Menu>
    </Layout.Sider>
    <Layout>
      <Layout.Header style="background: #fff">
        <menu-unfold-outlined
          v-if="collapsed"
          @click="() => (collapsed = !collapsed)"
        />
        <menu-fold-outlined
          v-else
          @click="() => (collapsed = !collapsed)"
        />
      </Layout.Header>
      <Layout.Content
        :style="{
          margin: '24px 16px',
          padding: '24px',
          background: '#fff',
          minHeight: '280px',
        }"
      >
        Content
      </Layout.Content>
    </Layout>
  </Layout>
</template>

<style scoped></style>
