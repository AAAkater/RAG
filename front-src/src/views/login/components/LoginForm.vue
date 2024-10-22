<script lang="ts" setup>
import { h, toRaw, ref } from "vue"
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
import { refreshCaptcha } from "@/api"
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
      pattern: /^[A-Za-z]{3,8}$/,
      message: "账号必须为3到8位字符",
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
// const getCaptchaItem = async () => {
//   const resp = await getCaptcha()

//   if (resp.status !== 200 || resp.data.code !== "0") {
//     return
//   }
//   // console.log("获取验证码")
//   const { captchaId, captchaImgBase64 } = resp.data.data!
//   modelRef.captcha.id = captchaId
//   modelRef.captcha.base64 = captchaImgBase64
// }
// getCaptchaItem()

// 点击验证码图片刷新验证码
const onCaptchaClick = async () => {
  const resp = await refreshCaptcha(captcha.value.id)

  if (resp.status !== 200 || resp.data.code !== "0") {
    return
  }
  const { captchaId, captchaImgBase64 } = resp.data.data!
  captcha.value.id = captchaId
  captcha.value.base64 = captchaImgBase64
}

const onSubmit = async () => {
  validate()
    .then(() => {
      console.log(toRaw(modelRef))
    })
    .catch((err) => {
      console.log("error", err)
    })
  // console.log("校验ok")

  // try {
  //   const resp = await userLogin({
  //     username: modelRef.username,
  //     password: modelRef.password,
  //     captchaId: modelRef.captcha.id,
  //     captchaCode: modelRef.captcha.code,
  //   })

  //   if (resp.status !== 200) {
  //     throw new Error("登录失败")
  //   }

  //   // if (resp.status === 404) {
  //   //   throw new Error("登录失败")
  //   // }
  //   // 存储token
  //   userStore.updateToken(
  //     resp.data.data!.access_token,
  //     resp.data.data!.refresh_token,
  //   )
  //   // 更新user
  //   userStore.updateInfo(modelRef)
  //   message.success("登录成功")
  //   router.push("/dashboard")
  // } catch (err) {
  //   message.error()
  //   console.log(err)
  // }
}
const onRegisterClick = () => {
  router.push("/register")
}
const onForgotClick = () => {
  message.warning("我还在写QAQ")
}
</script>

<template>
  <Form
    :wrapper-col="{ span: 24 }"
    autocomplete="off"
  >
    <!-- 登录框 -->
    <Form.Item v-bind="validateInfos.username">
      <Input
        v-model:value="modelRef.username"
        placeholder="账号"
        :prefix="h(UserOutlined)"
      />
    </Form.Item>
    <!-- 密码框 -->
    <Form.Item v-bind="validateInfos.password">
      <Input.Password
        v-model:value="modelRef.password"
        placeholder="密码"
        :prefix="h(LockOutlined)"
      />
    </Form.Item>
    <!-- 验证码 -->
    <Space>
      <Form.Item v-bind="validateInfos.captcha_code">
        <Input
          v-model:value="modelRef.captcha_code"
          placeholder="验证码"
          :controls="false"
          :prefix="h(SafetyCertificateOutlined)"
        />
      </Form.Item>
      <Form.Item>
        <Image
          :src="`data:image/png;base64,${captcha.base64}`"
          @click="onCaptchaClick"
          :preview="false"
          fallback=""
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
