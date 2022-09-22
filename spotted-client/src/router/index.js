import { createRouter, createWebHashHistory } from "vue-router";
import Home from "@/views/Home.vue";
import Explore from "@/views/Explore.vue";
import Manage from "@/views/Manage.vue";
import NotFound from "@/views/NotFound.vue";

const routes = [
  {
    name: "home",
    path: "/",
    component: Home,
  },
  { name: "login", path: "/login", component: Home },
  { name: "explore", path: "/explore", component: Explore },
  {
    name: "manage",
    path: "/manage/profile",
    alias: "/manage",
    component: Manage,
  },
  {
    name: "newSubmission",
    path: "/manage/newsubmission",
    component: Manage,
  },
  {
    name: "mySubmissions",
    path: "/manage/mysubmissions",
    component: Manage,
  },
  {
    name: "myComments",
    path: "/manage/mycomments",
    component: Manage,
  },
  { name: "NotFound", path: "/:pathMatch(.*)*", component: NotFound },
];

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
  linkExactActiveClass: "text-yellow-500",
});

export default router;
