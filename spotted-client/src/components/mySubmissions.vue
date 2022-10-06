<template>
  <div class="toast toast-top toast-end mt-20" v-if="toast_show">
    <div class="alert" :class="toast_variant">
      <div>
        <font-awesome-icon icon="fa-solid fa-circle-info" class="my-2" />
        <span>{{ toast_msg }}</span>
      </div>
    </div>
  </div>
  <div class="m-auto" v-if="this.is_loading">
    <font-awesome-icon
      icon="fa-solid fa-spinner"
      class="fa-spin text-accent"
      size="3x"
    />
  </div>
  <div class="overflow-y-auto break-all">
    <div class="m-auto" v-if="this.markers.length === 0 && !this.is_loading">
      You have no submissions.
    </div>
    <table
      v-else-if="this.markers.length > 0 && !this.is_loading"
      class="table table-zebra text-center w-full"
    >
      <!-- head -->
      <thead>
        <tr>
          <th class="w-2/12">Select</th>
          <th class="w-2/12">Title</th>
          <th class="max-w-screen-md">Description</th>
          <th class="w-2/12">Upvotes</th>
          <th class="w-2/12">Photo</th>
          <th class="w-2/12">Actions</th>
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
          <td class="min-w-[12rem] max-w-[20rem] whitespace-normal">
            {{ marker.desc }}
          </td>
          <td>{{ marker.upvotes }}</td>
          <td>
            <img
              v-if="marker.photoUrls.length > 0"
              :src="marker.photoUrls[0]"
              alt="Marker Photo"
              class="max-w-15 m-auto"
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
              @click.prevent="deleteEntry(marker.muid)"
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
          <th>Upvotes</th>
          <th>Photo</th>
          <th>Actions</th>
        </tr>
      </thead>
    </table>
  </div>
</template>

<script>
import { mapStores, mapActions } from "pinia";
import useUserStore from "@/stores/user";
import useMapMarkersStore from "@/stores/mapMarkers.js";
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
      toast_show: false,
      toast_variant: "alert-success",
      toast_msg: "Success!",
    };
  },
  computed: {
    ...mapStores(useUserStore, useMapMarkersStore),
  },
  methods: {
    ...mapActions(useMapMarkersStore, {
      updateVisibility: "updateVisibility",
      deleteMarker: "deleteMarker",
    }),
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
    async changeVisibility(muid, isVisible) {
      try {
        await this.updateVisibility(muid, isVisible);
        this.toast_show = true;
        this.toast_msg = "Updated!";
      } catch (error) {
        console.log(error);
        this.toast_show = true;
        this.toast_variant = "alert-error";
        this.toast_msg = "Error!";
      }
      setTimeout(() => {
        this.toast_show = false;
        this.getMarkers();
      }, 2000);
    },
    async deleteEntry(muid) {
      try {
        await this.deleteMarker(muid);
        this.toast_show = true;
        this.toast_msg = "Deleted!";
      } catch (error) {
        console.log(error);
        this.toast_show = true;
        this.toast_variant = "alert-error";
        this.toast_msg = "Error!";
      }
      setTimeout(() => {
        this.toast_show = false;
        this.getMarkers();
      }, 2000);
    },
  },
  beforeMount() {
    this.getMarkers();
  },
};
</script>
