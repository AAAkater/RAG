<script lang="ts" setup>
import type { RegisterFormState } from "@/types"
import {
  LockOutlined,
  MailOutlined,
  SafetyCertificateOutlined,
} from "@ant-design/icons-vue"
import { Button, Form, Input, message, Space } from "ant-design-vue"
import type { Rule } from "ant-design-vue/es/form"
import { h, ref } from "vue"
import { useRouter } from "vue-router"
const router = useRouter()
const useForm = Form.useForm
const sendButton = ref({
  isDisable: false,
  content: "发送",
})
// 表单数据
const modelRef = ref<RegisterFormState>({
  email: "",
  password: "",
  email_code: "",
})
// 表单校验规则
const rulesRef = ref<Record<string, Rule[]>>({
  email: [
    {
      required: true,
      type: "email",
      message: "请输入正确的邮箱格式",
      trigger: ["blur", "change"],
    },
  ],
  password: [
    {
      required: true,
      message: "请输入密码",
      trigger: ["blur", "change"],
    },
  ],
  email_code: [
    {
      required: true,
      message: "请输入邮箱验证码",
      trigger: ["blur", "change"],
    },
  ],
})
const { resetFields, validate, validateInfos } = useForm(modelRef, rulesRef)

// 发送邮件验证码
const getEmailCaptcha = async () => {
  try {
    const _res = await validate("email")
  } catch (_err) {
    message.error("错误的邮箱格式")
    resetFields() //清空表单
    return
  }
  // 倒数60s
  let timer: number
  const startCountdown = () => {
    let countdown = 60
    sendButton.value.isDisable = true
    sendButton.value.content = `${countdown}s`

    timer = setInterval(() => {
      countdown--
      sendButton.value.content = `${countdown}s`
      if (countdown <= 0) {
        clearInterval(timer)
        sendButton.value.isDisable = false
        sendButton.value.content = `发送`
      }
    }, 1000)
  }
  startCountdown()
  message.info("邮箱验证码已发送")
}

// 点击注册
const onSubmit = async () => {
  try {
    const _res = await validate()
  } catch (_err) {
    message.error("请输入正确的信息")
    resetFields() //清空表单
    return
  }
  message.info("注册成功")
}
// 回到登录
const onLoginClick = () => {
  router.push("/login")
}
</script>

<template>
  <Form
    autocomplete="off"
    class="w-[225px]"
  >
    <!-- 邮箱 -->
    <Form.Item v-bind="validateInfos.email">
      <Input
        v-model:value="modelRef.email"
        placeholder="邮箱"
        :show-count="true"
        :prefix="h(MailOutlined)"
      />
    </Form.Item>
    <!-- 密码 -->
    <Form.Item v-bind="validateInfos.password">
      <Input.Password
        v-model:value="modelRef.password"
        placeholder="密码"
        :show-count="true"
        :prefix="h(LockOutlined)"
      />
    </Form.Item>
    <!-- 验证码 -->
    <Form.Item v-bind="validateInfos.email_code">
      <Space>
        <Input
          v-model:value="modelRef.email_code"
          placeholder="邮箱验证码"
          :prefix="h(SafetyCertificateOutlined)"
        />
        <Button
          type="default"
          @click="getEmailCaptcha"
          :disabled="sendButton.isDisable"
        >
          {{ sendButton.content }}
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
