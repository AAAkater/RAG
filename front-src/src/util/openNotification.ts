import { CheckOutlined, ExclamationOutlined } from '@ant-design/icons-vue'
import type { NotificationPlacement } from 'ant-design-vue'
import { notification } from 'ant-design-vue'
import { h } from 'vue'
const openNotification = (placement: NotificationPlacement, desc: string, status: boolean) => {
  if (status)
    notification.open({
      message: `操作成功`,
      description: desc,
      placement,
      icon: () => h(CheckOutlined, { style: 'color: green' }),
      duration: 3
    })
  else
    notification.open({
      message: `请求错误！`,
      description: desc,
      placement,
      icon: () => h(ExclamationOutlined, { style: 'color: red' }),
      duration: 3
    })
}

export default openNotification
