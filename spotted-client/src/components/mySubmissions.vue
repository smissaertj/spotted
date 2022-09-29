<template>
  <div class="overflow-x-auto">
    <table class="table table-zebra w-full">
      <!-- head -->
      <thead>
        <tr>
          <th>Title</th>
          <th>Description</th>
          <th>Visibility</th>
          <th>Photo</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <!-- rows -->
        <tr v-for="marker in markers" :key="marker">
          <td>{{ marker.title }}</td>
          <td>{{ marker.desc }}</td>
          <td>{{ marker.visibility }}</td>
          <td>
            <img :src="marker.photoUrls[0]" alt="Marker Photo" class="w-10" />
          </td>
          <td>
            <button class="btn btn-ghost btn-xs hover:btn-error">Delete</button>
            <button class="btn btn-ghost btn-xs mx-2 hover:btn-warning">
              Hide
            </button>
          </td>
        </tr>
      </tbody>
      <thead>
        <tr>
          <th>Title</th>
          <th>Description</th>
          <th>Visibility</th>
          <th>Photo</th>
          <th>Actions</th>
        </tr>
      </thead>
    </table>
  </div>
</template>

<script>
import { mapStores } from "pinia";
import useUserStore from "@/stores/user";
import { auth } from "@/includes/firebase";
import axios from "axios";
const authService = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});
export default {
  name: "mySubmissions",
  components: {},
  data() {
    return {
      markers: [],
    };
  },
  computed: {
    ...mapStores(useUserStore),
  },
  methods: {
    async getMarkers() {
      try {
        if (auth.currentUser) {
          const result = await authService.post(
            "/markers/" + this.userStore.uid
          );
          this.markers = result.data;
        } else {
          throw "Not authenticated";
        }
      } catch (error) {
        console.log(error);
      }
    },
  },
  beforeMount() {
    this.getMarkers();
  },
};
</script>
