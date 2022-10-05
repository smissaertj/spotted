import { defineStore } from "pinia";
import {
  auth,
  db,
  mapMarkerCollection,
  photoCollection,
} from "@/includes/firebase";
import axios from "axios";

const authService = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export default defineStore("mapMarkers", {
  state: () => ({
    markers: [],
    tmp_marker: [],
    center: { lat: -20.1609, lng: 57.5012 },
  }),
  actions: {
    async addNewMarker(markerData) {
      const docRef = await mapMarkerCollection.add(markerData);
      const markerID = docRef.id;
      docRef.update({ muid: markerID }); // Set the document id as a field in the document

      markerData.photoIDs.forEach((id) => {
        const docRef = photoCollection.doc(id);
        docRef.update({ muid: markerID });
      });
    },
    async updateVisibility(muid, isVisible) {
      const docRef = await mapMarkerCollection.doc(muid);
      docRef.update({ isVisible: isVisible });
    },
    async deleteMarker(muid) {
      const docRef = await mapMarkerCollection.doc(muid);
      docRef.delete();

      const photoRefs = await photoCollection.where("muid", "==", muid).get();
      const batch = db.batch();
      photoRefs.forEach((doc) => {
        batch.delete(doc.ref);
      });
      await batch.commit();
    },
    async getMarkers() {
      const result = await authService.post("/markers");
      const markerData = result.data.concat(this.tmp_marker);
      this.markers = markerData;
    },
  },
});
