import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router"
const routes: RouteRecordRaw[] = [
  {
    path: "/",
    component: () => import("@/views/home/index.vue"),
  },
  {
    path: "/dashboard",
    component: () => import("@/views/dashboard/index.vue"),
  },
  {
    path: "/login",
    component: () => import("@/views/login/index.vue"),
  },
  {
    path: "/dialog",
    component: () => import("@/views/dialog/index.vue"),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
})

export default router
