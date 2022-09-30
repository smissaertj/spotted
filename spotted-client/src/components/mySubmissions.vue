<template>
  <div class="m-auto" v-if="this.is_loading">
    <font-awesome-icon
      icon="fa-solid fa-spinner"
      class="fa-spin text-accent"
      size="3x"
    />
  </div>
  <div class="overflow-x-auto">
    <div class="m-auto" v-if="this.markers.length === 0 && !this.is_loading">
      You have no submissions.
    </div>
    <table
      v-else-if="this.markers.length > 0 && !this.is_loading"
      class="table table-zebra w-full text-center"
    >
      <!-- head -->
      <thead>
        <tr>
          <th>Select</th>
          <th>Title</th>
          <th>Description</th>
          <th>Photo</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <!-- rows -->
        <tr v-for="marker in markers" :key="marker">
          <td>
            <label>
              <input
                type="checkbox"
                class="checkbox"
                v-model="marker.selected"
              />
            </label>
          </td>
          <td>{{ marker.title }}</td>
          <td>{{ marker.desc }}</td>
          <td>
            <img
              v-if="marker.photoUrls.length > 0"
              :src="marker.photoUrls[0]"
              alt="Marker Photo"
              class="w-10"
            />
          </td>
          <td>
            <div
              class="tooltip"
              data-tip="Hidden by Administrator"
              v-if="marker.isAdminHidden"
            >
              <button
                class="btn btn-ghost btn-xs"
                :disabled="marker.isAdminHidden"
                :class="{
                  'hover:btn-success': !marker.isVisible,
                  'hover:btn-warning': marker.isVisible,
                }"
                @click.prevent="
                  changeVisibility(marker.muid, !marker.isVisible)
                "
              >
                <font-awesome-icon icon="fa-solid fa-eye-slash" />
              </button>
            </div>
            <button
              v-else-if="!marker.isAdminHidden"
              class="btn btn-ghost btn-xs"
              :disabled="!marker.selected"
              :class="{
                'hover:btn-success': !marker.isVisible,
                'hover:btn-warning': marker.isVisible,
              }"
              @click.prevent="changeVisibility(marker.muid, !marker.isVisible)"
            >
              <font-awesome-icon
                icon="fa-solid fa-eye"
                v-if="!marker.isVisible"
              />
              <font-awesome-icon icon="fa-solid fa-eye-slash" v-else />
            </button>
            <button
              class="btn btn-ghost btn-xs hover:btn-error m-2"
              :disabled="!marker.selected"
              @click.prevent="deleteMarker(marker.muid, 'delete')"
            >
              Delete
            </button>
          </td>
        </tr>
      </tbody>
      <thead>
        <tr>
          <th>Select</th>
          <th>Title</th>
          <th>Description</th>
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
      is_loading: false,
    };
  },
  computed: {
    ...mapStores(useUserStore),
  },
  methods: {
    async getMarkers() {
      try {
        if (auth.currentUser) {
          this.is_loading = true;
          const result = await authService.post(
            "/markers/user/" + this.userStore.uid,
            { id_token: this.userStore.idToken }
          );
          this.markers = result.data;
          this.is_loading = false;
        } else {
          throw "Not authenticated";
        }
      } catch (error) {
        console.log(error);
      }
    },
    changeVisibility(muid, isVisible) {
      console.log(muid, isVisible);
    },
  },
  beforeMount() {
    this.getMarkers();
  },
};
</script>
