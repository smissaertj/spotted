<template>
  <div class="flex flex-col w-full h-screen">
    <div
      class="card flex shadow-2xl bg-base-100 glass rounded-box place-items-center m-auto"
    >
      <div class="card-body text-center">
        <h1 class="font-bold text-3xl">404 Not Found</h1>
        <p class="font-bold">
          The paths you walk down lead to the treasures you seek. But this one
          does not.
        </p>
        <router-link :to="{ name: 'home' }" class="btn btn-accent"
          >Home</router-link
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "appNotFound",
};
</script>
