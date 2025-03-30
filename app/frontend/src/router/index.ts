import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router"
const routes: RouteRecordRaw[] = [
  {
    path: "/",
    component: () => import("@/views/home/index.vue"),
  },
  {
    path: "/dashboard",
    component: () => import("@/views/dashboard/index.vue"),
    redirect: "/dashboard/home",
    children: [
      {
        path: "home",
        meta: {
          title: "主页",
          noAuth: true,
        },
        component: () => import("@/views/dashboard/home/index.vue"),
      },
      {
        path: "knowledge-base",
        meta: {
          title: "知识库",
          noAuth: true,
        },
        component: () => import("@/views/dashboard/knowledge_base/index.vue"),
      },
      {
        path: "dialog",
        meta: {
          title: "对话",
          noAuth: true,
        },
        component: () => import("@/views/dashboard/dialog/index.vue"),
      },
    ],
  },
  {
    path: "/login",
    meta: {
      title: "登录",
      noAuth: true,
    },
    component: () => import("@/views/login/index.vue"),
  },
  {
    path: "/register",
    meta: {
      title: "注册",
      noAuth: true,
    },
    component: () => import("@/views/login/index.vue"),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
})

export default router
