<script lang="ts" setup>
import { h, onMounted, ref, toRaw } from "vue"
import {
  UserOutlined,
  LockOutlined,
  SafetyCertificateOutlined,
} from "@ant-design/icons-vue"
import { type Rule } from "ant-design-vue/es/form"
import {
  Form,
  Input,
  Image,
  Checkbox,
  Button,
  Space,
  message,
} from "ant-design-vue"
import { useUserStore } from "@/stores"
import { type LoginFormState } from "@/types"
import { useRouter } from "vue-router"
import { API } from "@/api"
import { AxiosError } from "axios"
import type { ErrorResponse } from "@/api/types/response"

const userStore = useUserStore()
const useForm = Form.useForm
const router = useRouter()
const captcha = ref({
  id: "",
  base64: "",
})
// 表单数据
const modelRef = ref<LoginFormState>({
  username: userStore.username,
  password: userStore.password,
  is_remember: false,
  captcha_code: "",
})

// 校验规则
const rulesRef = ref<Record<string, Rule[]>>({
  username: [
    {
      required: true,
      message: "请输入用户名",
      trigger: ["blur", "change"],
    },
    {
      pattern: /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/,
      message: "账号需为邮箱格式",
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
  captcha_code: [
    { required: true, message: "请输入验证码", trigger: ["blur", "change"] },
  ],
})

const { resetFields, validate, validateInfos } = useForm(modelRef, rulesRef)

// 获取验证码
const getCaptcha = async () => {
  try {
    const resp = await API.getCaptcha()
    if ("detail" in resp.data) {
      message.error(resp.data.detail)
      return
    }
    const { captchaId, captchaImgBase64 } = resp.data.data!
    captcha.value.id = captchaId
    captcha.value.base64 = captchaImgBase64
  } catch (err) {
    if (!(err instanceof AxiosError)) {
      message.error("未知错误")
      return
    }
    if (err.status === 500) {
      message.error("服务器内部错误")
      return
    }
    const errData = err.response?.data as ErrorResponse
    message.error(errData.detail)
  }
}

// 点击登录
const onSubmit = async () => {
  try {
    const _res = await validate()
  } catch (_err) {
    message.error("请输入正确的信息")
    resetFields() //清空表单
    return
  }
  try {
    const resp = await API.userLogin({
      username: modelRef.value.username,
      password: modelRef.value.password,
      captcha_id: captcha.value.id,
      captcha_code: modelRef.value.captcha_code,
    })

    if ("detail" in resp.data) {
      message.error(resp.data.detail)
      return
    }

    if (resp.data.code !== "0") {
      message.error(resp.data.msg)
      resetFields() //清空表单
      return
    }
    // 存储token
    userStore.updateToken(resp.data.data!.access_token)
    // 更新user
    userStore.updateInfo(toRaw(modelRef.value))
    message.success("登录成功")
    router.push("/dashboard")
  } catch (err) {
    if (!(err instanceof AxiosError)) {
      message.error("未知错误")
      return
    }
    if (err.status === 500) {
      message.error("服务器内部错误")
      return
    }
    const errData = err.response?.data as ErrorResponse
    message.error(errData.detail)
    // resetFields() //清空表单
  }
}
const onRegisterClick = () => {
  router.push("/register")
}
const onForgotClick = () => {
  message.warning("我还在写QAQ")
}

onMounted(async () => {
  await getCaptcha()
})
</script>

<template>
  <Form
    autocomplete="off"
    class="w-[225px]"
  >
    <!-- 登录框 -->
    <Form.Item v-bind="validateInfos.username">
      <Input
        v-model:value="modelRef.username"
        placeholder="账号"
        :show-count="true"
        :prefix="h(UserOutlined)"
      />
    </Form.Item>
    <!-- 密码框 -->
    <Form.Item v-bind="validateInfos.password">
      <Input.Password
        v-model:value="modelRef.password"
        placeholder="密码"
        :show-count="true"
        :prefix="h(LockOutlined)"
      />
    </Form.Item>
    <!-- 验证码 -->
    <Space>
      <Form.Item v-bind="validateInfos.captcha_code">
        <Input
          v-model:value="modelRef.captcha_code"
          placeholder="验证码"
          :prefix="h(SafetyCertificateOutlined)"
        />
      </Form.Item>
      <Form.Item>
        <Image
          :src="`data:image/png;base64,${captcha.base64}`"
          @click="getCaptcha"
          :preview="false"
          fallback=""
          height="28px"
          width="auto"
        />
      </Form.Item>
    </Space>
    <!-- 选项 -->
    <Form.Item>
      <div class="flex justify-between">
        <div>
          <Checkbox v-model:checked="modelRef.is_remember"> 记住我 </Checkbox>
        </div>
        <Button
          type="primary"
          html-type="submit"
          @click="onSubmit"
          >登录
        </Button>
      </div>
    </Form.Item>
    <!-- 注册与找回 -->
    <Form.Item>
      <div class="flex justify-between">
        <Button
          type="link"
          @click="onRegisterClick"
        >
          点击注册
        </Button>
        <Button
          @click="onForgotClick"
          type="link"
        >
          忘记密码?
        </Button>
      </div>
    </Form.Item>
  </Form>
</template>

<style scoped></style>
