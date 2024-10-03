<script lang="ts" setup>
import { reactive, ref } from "vue"
import {
  UserOutlined,
  LockOutlined,
  SafetyCertificateOutlined,
} from "@ant-design/icons-vue"
import { type Rule } from "ant-design-vue/es/form"
import {
  message,
  Form,
  Input,
  Space,
  Image,
  Flex,
  Checkbox,
  Button,
} from "ant-design-vue"
import { useUserStore } from "@/stores"
import { type FormState } from "@/types"
import captchaImg from "@/assets/image/captcha_example.jpeg"
import { useRouter } from "vue-router"
const userStore = useUserStore()
const router = useRouter()
// 表单数据
const formState = reactive<FormState>({
  username: "",
  password: "",
  captcha: "",
  remember: userStore.remember,
})
// 填写已有的信息
if (userStore.remember) {
  formState.username = userStore.username
  formState.password = userStore.password
}

const captchaSrc = ref("")
const getCaptcha = () => {
  // message.success("更新验证码")
  captchaSrc.value = captchaImg
}
getCaptcha()
// 校验规则
const rules: Record<string, Rule[]> = {
  username: [
    {
      required: true,
      message: "请输入账号",
    },
  ],
  password: [
    {
      required: true,
      message: "请输入密码",
    },
  ],
}

// 验证成功
const onFinish = (values: FormState) => {
  // message.loading("登录中", 0)

  console.log("Success:", values)
}
// 验证失败
// const onFinishFailed = (errorInfo: any) => {
//   console.log("Failed:", errorInfo)
// }

const submit = () => {
  // 更新user
  userStore.updateInfo(formState)
  message.success("登录成功")
  router.push("/dashboard")
}
</script>

<template>
  <div class="flex h-full w-1/2 items-center justify-center max-sm:w-full">
    <Form
      :model="formState"
      name="basic"
      :wrapper-col="{ span: 24 }"
      autocomplete="off"
      @finish="onFinish"
      :rules="rules"
    >
      <!-- 登录框 -->
      <Form.Item name="username">
        <Input
          v-model:value="formState.username"
          placeholder="账号"
        >
          <template #prefix>
            <UserOutlined style="color: rgba(0, 0, 0, 0.25)" />
          </template>
        </Input>
      </Form.Item>
      <!-- 密码框 -->
      <Form.Item name="password">
        <Input.Password
          v-model:value="formState.password"
          placeholder="密码"
        >
          <template #prefix>
            <LockOutlined style="color: rgba(0, 0, 0, 0.25)" />
          </template>
        </Input.Password>
      </Form.Item>
      <!-- 验证码 -->
      <Form.Item name="captcha">
        <Space>
          <Input
            v-model:value="formState.captcha"
            placeholder="验证码"
            :controls="false"
          >
            <template #prefix>
              <SafetyCertificateOutlined style="color: rgba(0, 0, 0, 0.25)" />
            </template>
          </Input>
          <Image
            :src="captchaSrc"
            @click="getCaptcha"
            :preview="false"
          />
        </Space>
      </Form.Item>
      <!-- 选项 -->
      <Form.Item name="remember">
        <Flex
          justify="space-between"
          align="center"
        >
          <div>
            <Checkbox v-model:checked="formState.remember"> 记住我 </Checkbox>
          </div>
          <Button
            type="primary"
            html-type="submit"
            @click="submit"
            >登录
          </Button>
        </Flex>
      </Form.Item>
      <!-- 注册与找回 -->
      <Form.Item>
        <Flex justify="space-between">
          <a href="">点击注册</a>
          <a href="">忘记密码?</a>
        </Flex>
      </Form.Item>
    </Form>
  </div>
</template>

<style scoped></style>
