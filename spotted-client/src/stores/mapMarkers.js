import { defineStore } from "pinia";
import { auth, mapMarkerCollection } from "@/includes/firebase";

export default defineStore("mapMarkers", {
  state: () => ({
    markers: [],
  }),
  actions: {
    async addNewMarker(markerData) {
      await mapMarkerCollection.doc().set(markerData);
    },
    async deleteMarker() {},
    async getAllMarkers() {},
  },
});
