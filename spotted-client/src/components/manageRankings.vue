<template>
  <div class="m-auto" v-if="this.is_loading">
    <font-awesome-icon
      icon="fa-solid fa-spinner"
      class="fa-spin text-accent"
      size="3x"
    />
  </div>
  <div class="overflow-y-auto break-all min-w-full">
    <div
      class="m-auto"
      v-if="this.orderedMarkers.length === 0 && !this.is_loading"
    >
      There are no rankings.
    </div>
    <table
      v-else-if="this.orderedMarkers.length > 0 && !this.is_loading"
      class="table table-zebra text-center w-full"
    >
      <!-- head -->
      <thead>
        <tr class="bg-accent">
          <th class="w-2/12 bg-accent-content/25 text-secondary-content">
            Rank
          </th>
          <th class="w-2/12 bg-accent-content/25 text-secondary-content">
            Title
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
        </tr>
      </thead>
      <tbody>
        <!-- rows -->
        <tr v-for="(marker, i) in orderedMarkers" :key="i">
          <td>
            {{ i + 1 }}
          </td>
          <td>{{ marker.title }}</td>
          <td>
            {{ marker.authority }}
            <div
              class="text-sm opacity-50"
              :class="{
                'text-success': marker.status === 'Resolved',
                'text-warning': marker.status === 'Reported',
              }"
            >
              {{ marker.status }}
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
        </tr>
      </tbody>
      <thead>
        <tr class="bg-accent">
          <th class="bg-accent-content/25 text-secondary-content">Rank</th>
          <th class="bg-accent-content/25 text-secondary-content">Title</th>
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
        </tr>
      </thead>
    </table>
  </div>
</template>

<script>
import { mapActions } from "pinia";
import useMapMarkersStore from "@/stores/mapMarkers.js";
import { mapStores } from "pinia/dist/pinia";
export default {
  name: "manageRankings.vue",
  computed: {
    ...mapStores(useMapMarkersStore),
    orderedMarkers: function () {
      return this.mapMarkersStore.markers.sort((a, b) => {
        return b.downvotes - a.downvotes;
      });
    },
  },
  methods: {
    ...mapActions(useMapMarkersStore, ["getMarkers"]),
    getAllMarkers() {
      this.getMarkers();
    },
  },
  mounted() {
    this.getAllMarkers();
  },
};
</script>

<style scoped></style>
