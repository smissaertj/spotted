import { createRouter, createWebHashHistory } from "vue-router";
import Home from "@/views/Home.vue";
import Login from "@/views/Login.vue";

const routes = [
  {
    name: "home",
    path: "/",
    component: Home,
  },
  { name: "login", path: "/login", component: Login },
];

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
