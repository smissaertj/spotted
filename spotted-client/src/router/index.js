import { createRouter, createWebHashHistory } from "vue-router";
import Home from "@/views/Home.vue";
import Explore from "@/views/Explore.vue";
import Manage from "@/views/Manage.vue";
import NotFound from "@/views/NotFound.vue";
import useUserStore from "@/stores/user.js";

const routes = [
  {
    name: "home",
    path: "/",
    component: Home,
  },
  { name: "login", path: "/login", component: Home },
  { name: "explore", path: "/explore", component: Explore },
  {
    name: "profile",
    path: "/manage/profile",
    component: Manage,
    meta: {
      requiresAuth: true,
    },
  },
  {
    name: "newSubmission",
    path: "/manage/newsubmission",
    alias: "/manage",
    component: Manage,
    meta: {
      requiresAuth: true,
    },
  },
  {
    name: "mySubmissions",
    path: "/manage/mysubmissions",
    component: Manage,
    meta: {
      requiresAuth: true,
    },
  },
  {
    name: "myComments",
    path: "/manage/mycomments",
    component: Manage,
    meta: {
      requiresAuth: true,
    },
  },
  { name: "NotFound", path: "/:pathMatch(.*)*", component: NotFound },
];

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
  linkExactActiveClass: "text-yellow-500",
});

router.beforeEach((to, from, next) => {
  if (!to.meta.requiresAuth) {
    next();
    return;
  }
  const store = useUserStore();
  if (store.userLoggedIn) {
    next();
  } else {
    next({ name: "home" });
  }
});

export default router;
