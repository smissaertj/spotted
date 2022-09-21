<template>
  <header id="header" class="w-full">
    <div class="navbar bg-base-100">
      <div class="navbar-start">
        <router-link
          :to="{ name: 'home' }"
          class="btn btn-ghost normal-case text-xl"
          >Spotted!<font-awesome-icon icon="fa-solid fa-splotch" class="m-1"
        /></router-link>
      </div>
      <div class="navbar-center hidden lg:flex">
        <ul class="menu menu-horizontal p-0">
          <li><a class="link link-accent link-hover">About</a></li>
          <li><a class="link link-accent link-hover">Explore</a></li>
        </ul>
      </div>
      <div class="navbar-end">
        <router-link
          :to="{ name: 'login' }"
          class="btn"
          v-if="this.$route.name == 'home'"
          >Login</router-link
        >
        <router-link
          :to="{ name: 'home' }"
          class="btn"
          v-if="this.$route.name == 'login'"
          >Register</router-link
        >
      </div>
    </div>
  </header>
</template>
<script>
export default {
  name: "AppHeader",
};
</script>
