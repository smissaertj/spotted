<template>
  <div class="hero h-screen bg-base-100 rounded">
    <div class="hero-overlay bg-opacity-65"></div>
    <div class="hero-content sm:flex-col md:flex-row">
      <div class="card w-full glass m-auto" v-if="!userStore.userLoggedIn">
        <div class="card-body">
          <h2 class="card-title">Create</h2>
          <font-awesome-icon icon="fa-solid fa-map-location-dot" size="3x" />
          <p class="my-2 font-bold">
            Pin locations, add descriptions, upload pictures.
          </p>
          <div class="card-actions justify-end">
            <router-link class="btn btn-primary" :to="{ name: 'explore' }"
              >Explore
            </router-link>
          </div>
        </div>
      </div>
      <app-register
        v-if="this.$route.name == 'home' && !userStore.userLoggedIn"
      />
      <app-login
        v-else-if="this.$route.name == 'login' && !userStore.userLoggedIn"
      />
      <div
        class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-300 m-auto"
        v-else-if="userStore.userLoggedIn"
      >
        <div class="card-body bg-base-300">
          <h1 class="text-5xl text-center">
            Welcome {{ userStore.displayName }}!
          </h1>
          <router-link
            :to="{ name: 'newSubmission' }"
            class="btn btn-accent btn-block mt-4"
            >Get Started</router-link
          >
        </div>
      </div>

      <div
        class="card w-full sm:w-100 glass m-auto"
        v-if="!userStore.userLoggedIn"
      >
        <div class="card-body">
          <h2 class="card-title">Explore</h2>
          <font-awesome-icon
            icon="fa-solid fa-magnifying-glass-location"
            size="3x"
          />
          <p class="my-2 font-bold">Explore and upvote submissions.</p>
          <div class="card-actions justify-end">
            <router-link class="btn btn-primary" :to="{ name: 'explore' }"
              >Explore
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import useUserStore from "@/stores/user.js";
import { mapStores } from "pinia";
import appRegister from "@/components/appRegister.vue";
import appLogin from "@/components/appLogin.vue";

export default {
  name: "appHome",
  components: { appRegister, appLogin },
  computed: {
    ...mapStores(useUserStore),
  },
};
</script>

<style scoped>
.hero {
  background-image: url(../assets/hero_bg.jpg);
  background-size: cover;
}
</style>
