<template>
  <div
    class="hero h-screen bg-base-100 rounded"
    style="
      background-image: url(src/assets/hero_bg.jpg);
      background-size: cover;
    "
  >
    <div class="hero-overlay bg-opacity-65"></div>
    <div class="hero-content sm:flex-col md:flex-row">
      <div class="card w-full glass m-auto">
        <div class="card-body">
          <h2 class="card-title">Create</h2>
          <font-awesome-icon icon="fa-solid fa-map-location-dot" size="3x" />
          <p class="my-2 font-bold">
            Pin locations, add descriptions, upload pictures.
          </p>
          <div class="card-actions justify-end">
            <a href="/about">
              <button class="btn btn-primary">Learn more</button>
            </a>
          </div>
        </div>
      </div>
      <app-register v-if="this.$route.name == 'home'" />
      <app-login v-if="this.$route.name == 'login'" />

      <div class="card w-full sm:w-100 glass m-auto">
        <div class="card-body">
          <h2 class="card-title">Explore</h2>
          <font-awesome-icon
            icon="fa-solid fa-magnifying-glass-location"
            size="3x"
          />
          <p class="my-2 font-bold">Explore and participate in discussions.</p>
          <div class="card-actions justify-end">
            <a href="/about">
              <button class="btn btn-primary">Learn more</button>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import appRegister from "@/components/appRegister.vue";
import appLogin from "@/components/appLogin.vue";
export default {
  name: "appHome",
  components: { appRegister, appLogin },
};
</script>
