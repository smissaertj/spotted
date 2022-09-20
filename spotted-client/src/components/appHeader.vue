<template>
  <header id="header" class="w-full">
    <div class="navbar bg-base-content/25">
      <div class="navbar-start">
        <a class="btn btn-ghost normal-case text-xl"
          >Spotted!<font-awesome-icon icon="fa-solid fa-splotch" class="m-1"
        /></a>
      </div>
      <div class="navbar-center hidden lg:flex">
        <ul class="menu menu-horizontal p-0">
          <li><a class="link link-neutral link-hover">About</a></li>
          <li><a class="link link-neutral link-hover">Explore</a></li>
        </ul>
      </div>
      <div class="navbar-end">
        <router-link :to="{ name: 'login' }" class="btn">Login</router-link>
      </div>
    </div>
  </header>
</template>
<script>
export default {
  name: "AppHeader",
};
</script>
