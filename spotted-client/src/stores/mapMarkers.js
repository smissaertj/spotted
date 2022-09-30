import { defineStore } from "pinia";
import { auth, mapMarkerCollection } from "@/includes/firebase";
import axios from "axios";

export default defineStore("mapMarkers", {
  state: () => ({
    markers: [],
  }),
  actions: {
    async addNewMarker(markerData) {
      const docRef = await mapMarkerCollection.add(markerData);
      docRef.update({ muid: docRef.id }); // Set the document id as a field in the document
    },
    async updateVisibility(muid, isVisible) {
      const docRef = await mapMarkerCollection.doc(muid);
      docRef.update({ isVisible: isVisible });
    },
    async deleteMarker(muid) {
      const docRef = await mapMarkerCollection.doc(muid);
      docRef.delete();
    },
  },
});
