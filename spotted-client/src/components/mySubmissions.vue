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
  <div class="overflow-y-auto break-all min-w-full">
    <div class="m-auto" v-if="this.markers.length === 0 && !this.is_loading">
      You have no submissions.
    </div>
    <table
      v-else-if="this.markers.length > 0 && !this.is_loading"
      class="table table-zebra text-center w-full"
    >
      <!-- head -->
      <thead>
        <tr class="bg-accent">
          <th class="w-2/12 bg-accent-content/25 text-secondary-content">
            Select
          </th>
          <th class="w-2/12 bg-accent-content/25 text-secondary-content">
            Title
          </th>
          <th
            class="max-w-screen-md bg-accent-content/25 text-secondary-content"
          >
            Description
          </th>
          <th class="bg-accent-content/25 text-secondary-content">
            Reported to
          </th>
          <th class="w-2/12 bg-accent-content/25 text-secondary-content">
            <font-awesome-icon
              icon="fa-solid fa-thumbs-down"
              class="text-accent-content mr-2"
              size="2x"
            />
          </th>
          <th class="w-2/12 bg-accent-content/25 text-secondary-content">
            Photo
          </th>
          <th class="w-2/12 bg-accent-content/25 text-secondary-content">
            Actions
          </th>
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
          <td>
            {{ marker.authority }}
            <div class="text-sm opacity-50">
              <select
                type="select"
                class="input w-full text-sm"
                :class="{
                  'text-success': marker.status === 'Resolved',
                  'text-warning': marker.status === 'Reported',
                }"
                name="statusSelect"
                @change.prevent="updateMarkerStatus(marker.muid, $event)"
              >
                <option value="{{ marker.status }}" disabled selected>
                  {{ marker.status }}
                </option>
                <option value="Reported" class="text-warning">Reported</option>
                <option value="Resolved" class="text-success">Resolved</option>
              </select>
            </div>
          </td>
          <td>{{ marker.downvotes }}</td>
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
        <tr class="bg-accent">
          <th class="bg-accent-content/25 text-secondary-content">Select</th>
          <th class="bg-accent-content/25 text-secondary-content">Title</th>
          <th class="bg-accent-content/25 text-secondary-content">
            Description
          </th>
          <th class="bg-accent-content/25 text-secondary-content">
            Reported to
          </th>
          <th class="bg-accent-content/25 text-secondary-content">
            <font-awesome-icon
              icon="fa-solid fa-thumbs-down"
              class="text-accent-content mr-2"
              size="2x"
            />
          </th>
          <th class="bg-accent-content/25 text-secondary-content">Photo</th>
          <th class="bg-accent-content/25 text-secondary-content">Actions</th>
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
      updateStatus: "updateStatus",
    }),
    async updateMarkerStatus(muid, event) {
      try {
        const newStatus = event.target.value;
        await this.updateStatus(muid, newStatus);
        setTimeout(() => {
          this.toast_show = false;
          this.getMarkers();
        }, 2000);
      } catch (error) {
        console.log(error);
      }
    },
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
      }, 1000);
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
