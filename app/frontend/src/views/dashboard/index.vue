<script lang="ts" setup>
import { ref } from "vue"
import { MenuUnfoldOutlined, MenuFoldOutlined } from "@ant-design/icons-vue"
import MenuLogo from "./components/MenuLogo.vue"
import SideMenu from "./components/SideMenu.vue"
import { Layout } from "ant-design-vue"
const collapsed = ref<boolean>(true)
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
      <SideMenu />
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
