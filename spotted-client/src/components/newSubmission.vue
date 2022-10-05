<template>
  <app-google-map @add-marker="newMarker($event)" :key="componentKey" />
  <div class="flex flex-col w-full m-auto">
    <h1 class="text-center text-3xl mt-4">Add a new location</h1>
    <p class="text-center text-accent">
      Click on the map to place a new Marker, then submit the form.
    </p>
    <div class="w-1/3 mt-4 m-auto">
      <vee-form
        class="form-control w-full"
        @submit="submitNewLocation"
        :validation-schema="submitSchema"
      >
        <vee-field
          type="number"
          placeholder="Lat"
          class="input input-bordered w-full"
          name="lat"
          required
          v-model="markerData.lat"
          hidden
        />
        <vee-field
          type="number"
          placeholder="Long"
          class="input input-bordered w-full"
          name="long"
          required
          v-model="markerData.long"
          hidden
        />
        <div class="form-control">
          <vee-field
            type="text"
            placeholder="Title"
            class="input input-bordered w-full"
            name="title"
            required
            v-model="markerData.title"
          />
          <ErrorMessage class="text-red-600" name="title" />
        </div>
        <div class="form-control mt-2">
          <vee-field
            as="textarea"
            class="textarea textarea-bordered"
            placeholder="Description"
            name="description"
            required
            v-model="markerData.desc"
          />
          <ErrorMessage class="text-red-600" name="description" />
        </div>
        <div class="form-control mt-2">
          <vee-field
            as="select"
            type="select"
            placeholder="Category"
            class="input input-bordered w-full"
            name="category"
            required
            v-model="markerData.category"
          >
            <option value="" disabled selected>Category</option>
            <option value="Environment">Environment</option>
            <option value="Public Infrastructure">Public Infrastructure</option>
            <option value="Safety Concern">Safety Concern</option>
          </vee-field>
          <ErrorMessage class="text-red-600" name="category" />
        </div>
        <div class="p-2">
          <!-- Upload Dropbox -->
          <div
            class="w-full p-2 rounded text-center cursor-pointer border border-dashed border-gray-400 text-gray-400 transition duration-500 hover:text-white hover:bg-secondary hover:border-secondary hover:border-solid"
            :class="{
              'bg-secondary border-solid': is_dragover,
            }"
            @drag.prevent.stop=""
            @dragstart.prevent.stop=""
            @dragend.prevent.stop="is_dragover = false"
            @dragover.prevent.stop="is_dragover = true"
            @dragenter.prevent.stop="is_dragover = true"
            @dragleave.prevent.stop="is_dragover = leave"
            @drop.prevent.stop="upload($event)"
          >
            <p class="font-bold text-accent">Drag & Drop your photos here.</p>
            <p>Supports JPG files up to 10Mb.</p>
            <!-- Progess Bars -->
            <div class="mb-4" v-for="upload in uploads" :key="uploads.name">
              <!-- File Name -->
              <div class="font-bold text-sm" :class="upload.text_class">
                <i :class="upload.icon"></i>{{ upload.name }}
              </div>
              <div class="flex h-2 overflow-hidden bg-base-100 rounded">
                <!-- Inner Progress Bar -->
                <progress
                  class="progress w-full"
                  :value="upload.current_progress"
                  max="100"
                  :class="upload.variant"
                  :style="{ width: upload.current_progress + '%' }"
                ></progress>
              </div>
            </div>
          </div>
        </div>
        <div class="form-control mt-2">
          <button
            class="btn btn-primary"
            type="submit"
            :disabled="in_submission"
          >
            Submit
          </button>
          <div
            class="alert shadow-lg mt-2 justify-center font-bold"
            :class="submit_alert_variant"
            v-if="submit_show_alert"
          >
            <div>
              <span
                ><font-awesome-icon
                  icon="fa-solid fa-spinner"
                  class="fa-spin mr-2"
                  v-if="submit_alert_variant == 'alert-warning'"
                />{{ submit_alert_msg }}</span
              >
            </div>
          </div>
        </div>
      </vee-form>
    </div>
  </div>
</template>

<script>
import { mapStores, mapActions } from "pinia";
import useUserStore from "@/stores/user";
import useMapMarkersStore from "@/stores/mapMarkers";
import appGoogleMap from "@/components/appGoogleMap.vue";
import { auth, storage, photoCollection } from "@/includes/firebase";

export default {
  name: "newSubmission",
  components: {
    appGoogleMap,
  },
  data() {
    return {
      submitSchema: {
        title: "required",
        description: "required",
        category: "required",
      },
      in_submission: false,
      submit_show_alert: false,
      submit_alert_variant: "alert-success",
      submit_alert_msg: "",
      markerData: {
        title: "",
        desc: "",
        date: new Date().toISOString(),
        status: "Up To Date",
        category: "",
        isVisible: true,
        isAdminHidden: false,
        photoUrls: "",
      },
      is_dragover: false,
      uploads: [],
      photoIDs: [],
      photoUrlList: [],
      componentKey: 0,
    };
  },
  computed: {
    ...mapStores(useUserStore, useMapMarkersStore),
  },
  methods: {
    ...mapActions(useMapMarkersStore, ["addNewMarker", "getMarkers"]),
    newMarker(e) {
      const latLng = e.latLng.toJSON();

      this.markerData.position = latLng;
      this.mapMarkersStore.tmp_marker = [];
      this.mapMarkersStore.tmp_marker.push(this.markerData);
      this.getMarkers();
      this.componentKey += 1;
    },
    upload($event) {
      this.is_dragover = false;
      this.submit_show_alert = false;

      const files = [...$event.dataTransfer.files];
      files.forEach((file) => {
        if (file.type !== "image/jpeg") {
          this.submit_show_alert = true;
          this.submit_alert_variant = "alert-error";
          this.submit_alert_msg = `${file.type} is not an accepted type.`;
          return;
        }
        const storageRef = storage.ref();
        const fileRef = storageRef.child(`${this.userStore.uid}/${file.name}`);
        const task = fileRef.put(file);

        const uploadIndex =
          this.uploads.push({
            task,
            current_progress: 0,
            name: file.name,
            variant: "progress-accent",
            text_class: "",
          }) - 1;

        task.on(
          "state_changed",
          (snapshot) => {
            const progress =
              (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
            this.uploads[uploadIndex].current_progress = progress;
          },
          (error) => {
            this.uploads[uploadIndex].variant = "progress-error";
            this.uploads[uploadIndex].text_class = "text-red-400";
            console.log(error);
          },
          async () => {
            const photo = {
              uid: auth.currentUser.uid,
              muid: "",
              filename: task.snapshot.ref.name,
            };

            photo.url = await task.snapshot.ref.getDownloadURL();
            this.photoUrlList.push(photo.url);
            const docRef = await photoCollection.add(photo);
            this.photoIDs.push(docRef.id);

            this.uploads[uploadIndex].variant = "progress-success";
            this.uploads[uploadIndex].text_class = "text-green-100";
          }
        );
      });
    },
    async submitNewLocation() {
      try {
        this.in_submission = true;
        this.submit_show_alert = true;
        this.submit_alert_variant = "alert-warning";
        this.submit_alert_msg = "Submitting data...";
        const user = auth.currentUser;
        if (user) {
          if (this.photoUrlList.length === 0) {
            throw "Please add your photos.";
          }
          this.markerData.uid = this.userStore.uid;
          this.markerData.photoUrls = this.photoUrlList;
          this.markerData.photoIDs = this.photoIDs;
          await this.addNewMarker(this.markerData);
        } else {
          throw "Not authenticated.";
        }
        this.in_submission = false;
        this.submit_show_alert = true;
        this.submit_alert_variant = "alert-success";
        this.submit_alert_msg = "Thank you!";
        setTimeout(() => {
          this.submit_show_alert = false;
          Object.keys(this.markerData).forEach(
            (key) => (this.markerData[key] = "")
          );
          this.uploads = [];
          this.$router.push({ name: "mySubmissions" });
        }, 2000);
      } catch (error) {
        console.log(error);
        this.submit_alert_variant = "alert-error";
        this.submit_alert_msg = error;
        setTimeout(() => {
          this.submit_show_alert = false;
          this.in_submission = false;
        }, 2000);
      }
    },
  },
};
</script>
