<template>
  <app-google-map />
  <div
    class="flex flex-col shadow-2xl bg-base-100 glass h-1/2 w-full justify-items-center"
  >
    <h1 class="text-center text-3xl mt-4">Add a new location</h1>
    <p class="text-center">
      Click on the map to place a new Marker, then submit the form:
    </p>
    <div class="w-1/3 mt-4 m-auto">
      <vee-form class="form-control w-full" @submit="submitNewLocation">
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
          <label class="input-group">
            <span class="label-text">Title</span>

            <vee-field
              type="text"
              placeholder=""
              class="input input-bordered w-full"
              name="title"
              required
              v-model="markerData.title"
            />
          </label>
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
        <!--        <div class="form-control mt-2">-->
        <!--          <label class="input-group">-->
        <!--            <span class="label-text">Category</span>-->
        <!--            <vee-field-->
        <!--              as="select"-->
        <!--              type="select"-->
        <!--              placeholder=""-->
        <!--              class="input input-bordered w-full"-->
        <!--              name="category"-->
        <!--              required-->
        <!--            >-->
        <!--              <option value="">Coffee</option>-->
        <!--              <option value="">Tea</option>-->
        <!--              <option value="">Coke</option>-->
        <!--            </vee-field>-->
        <!--          </label>-->
        <!--          <ErrorMessage class="text-red-600" name="category" />-->
        <!--        </div>-->
        <div class="p-6">
          <!-- Upload Dropbox -->
          <div
            class="w-full px-10 py-10 rounded text-center cursor-pointer border border-dashed border-gray-400 text-gray-400 transition duration-500 hover:text-white hover:bg-green-400 hover:border-green-400 hover:border-solid"
            :class="{
              'bg-green-400 border-green-400 border-solid': is_dragover,
            }"
            @drag.prevent.stop=""
            @dragstart.prevent.stop=""
            @dragend.prevent.stop="is_dragover = false"
            @dragover.prevent.stop="is_dragover = true"
            @dragenter.prevent.stop="is_dragover = true"
            @dragleave.prevent.stop="is_dragover = leave"
            @drop.prevent.stop="upload($event)"
          >
            <h5>Drag & Drop your photos here</h5>
          </div>
          <!-- Progess Bars -->
          <div class="mb-4" v-for="upload in uploads" :key="uploads.name">
            <!-- File Name -->
            <div class="font-bold text-sm" :class="upload.text_class">
              <i :class="upload.icon"></i>{{ upload.name }}
            </div>
            <div class="flex h-4 overflow-hidden bg-gray-200 rounded">
              <!-- Inner Progress Bar -->
              <div
                class="transition-all progress-bar"
                :class="upload.variant"
                :style="{ width: upload.current_progress + '%' }"
              ></div>
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
import { auth } from "@/includes/firebase";
export default {
  name: "newSubmission",
  components: {
    appGoogleMap,
  },
  data() {
    return {
      in_submission: false,
      submit_show_alert: false,
      submit_alert_variant: "alert-success",
      submit_alert_msg: "",
      markerData: {
        title: "",
        desc: "",
        lat: "",
        long: "",
        date: new Date().toISOString(),
        status: "Up To Date",
      },
    };
  },
  computed: {
    ...mapStores(useUserStore),
  },
  methods: {
    ...mapActions(useMapMarkersStore, ["addNewMarker"]),
    async submitNewLocation(values) {
      try {
        this.in_submission = true;
        this.submit_show_alert = true;
        this.submit_alert_variant = "alert-warning";
        this.submit_alert_msg = "Submitting data...";
        const user = auth.currentUser;
        if (user) {
          this.markerData.uid = this.userStore.uid;
          console.log(this.markerData);
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

<style scoped></style>
