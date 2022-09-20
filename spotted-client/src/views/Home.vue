<template>
  <div
    class="hero h-1/2 bg-base-100 rounded"
    style="background-image: url(src/assets/hero_bg.jpg)"
  >
    <div class="hero-overlay bg-opacity-75"></div>
    <div class="hero-content flex-col lg:flex-row-reverse">
      <div class="text-center lg:text-left">
        <h1 class="text-5xl font-bold text-primary-content">Join us!</h1>
        <p class="py-6 text-2xl font-bold text-info-content">
          Become part of our vibrant community.
        </p>
      </div>
      <app-register />
    </div>
  </div>
  <div class="container flex flex-row sm:flex-wrap w-5/6 h-1/3 mx-auto m-auto">
    <div class="card w-1/4 glass m-auto">
      <div class="card-body">
        <h2 class="card-title">Create</h2>
        <font-awesome-icon icon="fa-solid fa-map-location-dot" size="3x" />
        <p class="my-2">Pin locations, add descriptions and upload pictures.</p>
        <div class="card-actions justify-end">
          <a href="/about">
            <button class="btn btn-primary">Learn more</button>
          </a>
        </div>
      </div>
    </div>
    <div class="card w-1/4 glass m-auto">
      <div class="card-body">
        <h2 class="card-title">Share</h2>
        <font-awesome-icon icon="fa-brands fa-slideshare" size="3x" />
        <p class="my-2">
          Share your contributions with friends on social media.
        </p>
        <div class="card-actions justify-end">
          <a href="/about">
            <button class="btn btn-primary">Learn more</button>
          </a>
        </div>
      </div>
    </div>
    <div class="card w-1/4 glass m-auto">
      <div class="card-body">
        <h2 class="card-title">Explore</h2>
        <font-awesome-icon
          icon="fa-solid fa-magnifying-glass-location"
          size="3x"
        />
        <p class="my-2">
          Explore & upvote locations, upvote and participate in discussions.
        </p>
        <div class="card-actions justify-end">
          <a href="/about">
            <button class="btn btn-primary">Learn more</button>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import appRegister from "@/components/appRegister.vue";
export default {
  name: "appHome",
  components: { appRegister },
};
</script>
