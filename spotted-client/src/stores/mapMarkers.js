import { defineStore } from "pinia";
import { auth, mapMarkerCollection } from "@/includes/firebase";

export default defineStore("mapMarkers", {
  state: () => ({
    markers: [],
  }),
  actions: {
    async addNewMarker(markerData) {
      console.log("adding a new marker");
      const photoUrlList = [];
      // TODO - Upload files
      markerData.photoUrlList = photoUrlList;
      await mapMarkerCollection.doc().set(markerData);
      console.log("Done adding new marker");
    },
    async deleteMarker() {},
    async getAllMarkers() {},
  },
});
