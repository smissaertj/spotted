<template>
  <header id="header" class="w-full">
    <div class="navbar bg-base-100">
      <div class="navbar-start">
        <router-link
          :to="{ name: 'home' }"
          class="btn btn-ghost normal-case text-xl"
          exact-active-class="no-active"
          >Spotted!<font-awesome-icon icon="fa-solid fa-binoculars" class="m-1"
        /></router-link>
      </div>
      <div class="navbar-center hidden lg:flex">
        <p class="font-bold text-accent">Share Locations of Interest</p>
      </div>
      <div class="navbar-end">
        <ul class="menu menu-horizontal p-0 m-0">
          <li>
            <router-link
              class="link link-accent link-hover"
              :to="{ name: 'explore' }"
              v-if="this.$route.name != 'home' && this.$route.name != 'login'"
              >Explore</router-link
            >
          </li>
          <li>
            <router-link
              class="link link-accent link-hover mx-2"
              :to="{ name: 'newSubmission' }"
              v-if="userStore.userLoggedIn"
              >Manage</router-link
            >
          </li>
          <li>
            <button
              @click.prevent="signOut"
              class="btn"
              v-if="userStore.userLoggedIn"
            >
              Sign Out
            </button>
          </li>
        </ul>
      </div>
    </div>
  </header>
</template>
<script>
import { mapStores } from "pinia";
import useUserStore from "@/stores/user";
export default {
  name: "AppHeader",
  computed: {
    ...mapStores(useUserStore),
  },
  methods: {
    signOut() {
      this.userStore.signOut();
      this.$router.push({ name: "home" });
    },
  },
};
</script>
