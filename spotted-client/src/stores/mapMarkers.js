import { defineStore } from "pinia";
import {
  auth,
  db,
  mapMarkerCollection,
  photoCollection,
} from "@/includes/firebase";
import axios from "axios";

export default defineStore("mapMarkers", {
  state: () => ({
    markers: [],
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
  },
});
