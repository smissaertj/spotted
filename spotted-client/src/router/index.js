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
    path: "/profile",
    component: Manage,
    meta: {
      requiresAuth: true,
    },
  },
  {
    name: "newSubmission",
    path: "/newsubmission",
    alias: "/manage",
    component: Manage,
    meta: {
      requiresAuth: true,
    },
  },
  {
    name: "mySubmissions",
    path: "/mysubmissions",
    component: Manage,
    meta: {
      requiresAuth: true,
    },
  },
  {
    name: "myComments",
    path: "/mycomments",
    component: Manage,
    meta: {
      requiresAuth: true,
    },
  },
  {
    name: "manageUsers",
    path: "/users",
    component: Manage,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    },
  },
  {
    name: "manageSubmissions",
    path: "/submissions",
    component: Manage,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    },
  },
  {
    name: "rankings",
    path: "/rankings",
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
  linkExactActiveClass: "text-accent",
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
