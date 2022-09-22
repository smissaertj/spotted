<template>
  <header id="header" class="w-full">
    <div class="navbar bg-base-100">
      <div class="navbar-start">
        <router-link
          :to="{ name: 'home' }"
          class="btn btn-ghost normal-case text-xl"
          exact-active-class="no-active"
          >Spotted!<font-awesome-icon icon="fa-solid fa-splotch" class="m-1"
        /></router-link>
      </div>
      <div class="navbar-center hidden lg:flex">
        <ul class="menu menu-horizontal p-0">
          <li>
            <router-link
              class="link link-accent link-hover"
              :to="{ name: 'explore' }"
              >Explore</router-link
            >
          </li>
          <li>
            <router-link
              class="link link-accent link-hover"
              :to="{ name: 'manage' }"
              v-if="userStore.userLoggedIn"
              >Manage</router-link
            >
          </li>
        </ul>
      </div>
      <div class="navbar-end">
        <router-link
          :to="{ name: 'login' }"
          class="btn"
          v-if="this.$route.name != 'login' && !userStore.userLoggedIn"
          >Login</router-link
        >
        <router-link
          :to="{ name: 'home' }"
          class="btn"
          v-else-if="this.$route.name != 'home' && !userStore.userLoggedIn"
          >Register</router-link
        >
        <button
          @click.prevent="signOut"
          class="btn"
          v-else-if="userStore.userLoggedIn"
        >
          Sign Out
        </button>
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
