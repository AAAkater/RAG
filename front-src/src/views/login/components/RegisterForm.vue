<script lang="ts" setup>
import {
  LockOutlined,
  MailOutlined,
  SafetyCertificateOutlined,
} from "@ant-design/icons-vue"
import { Button, Form, Input, message, Space } from "ant-design-vue"
import { h } from "vue"
import { useRouter } from "vue-router"
const router = useRouter()
const getEmailCaptcha = () => {}

const onSubmit = () => {
  message.info("我是注册")
}

const onLoginClick = () => {
  router.push("/login")
}
</script>

<template>
  <Form
    :wrapper-col="{ span: 24 }"
    autocomplete="off"
  >
    <Form.Item>
      <Input
        placeholder="邮箱"
        :prefix="h(MailOutlined)"
      />
    </Form.Item>
    <Form.Item>
      <Input
        placeholder="密码"
        :prefix="h(LockOutlined)"
      />
    </Form.Item>
    <Form.Item>
      <Space>
        <Input
          placeholder="验证码"
          :prefix="h(SafetyCertificateOutlined)"
        />
        <Button
          type="default"
          @click="getEmailCaptcha"
        >
          发送
        </Button>
      </Space>
    </Form.Item>
    <Form.Item>
      <div class="flex justify-between">
        <Button
          type="link"
          @click="onLoginClick"
        >
          回到登录
        </Button>
        <Button
          type="primary"
          @click="onSubmit"
        >
          注册
        </Button>
      </div>
    </Form.Item>
  </Form>
</template>

<style lang="css" scoped></style>
