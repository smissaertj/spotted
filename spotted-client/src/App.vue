<template>
  <app-header />
  <router-view></router-view>
  <app-footer />
</template>
<script>
import AppHeader from "@/components/appHeader.vue";
import AppFooter from "@/components/appFooter.vue";
export default {
  name: "App",
  components: {
    AppHeader,
    AppFooter,
  },
};
</script>
