<template>
  <GoogleMap
    :api-key="apikey"
    :center="center"
    :zoom="11"
    zoom-control-position="TOP_RIGHT"
    :styles="styles"
    class="w-full h-1/2"
    @click="$emit('addMarker', $event)"
  >
    <MarkerCluster>
      <Marker
        v-for="(marker, i) in markers"
        :options="{
          position: marker.position,
          label: marker.label,
          title: marker.title,
          clickable: marker.clickable,
        }"
        :key="i"
      >
        <InfoWindow
          class="text-accent-content w-fit glass"
          :options="{ content: 'TEST' }"
        >
          <div class="mockup-window border bg-base-300">
            <div class="flex flex-col justify-center px-4 py-4 bg-base-100">
              <h1 class="font-bold text-accent text-4xl m-2">
                {{ marker.title }}
              </h1>
              <div class="badge badge-lg badge-primary text-2xl m-2 font-bold">
                {{ marker.category }}
              </div>
              <p class="text-2xl text-accent-content">
                {{ marker.desc }}
              </p>
              <CustomControl position="CENTER">
                <button
                  class="btn btn-block btn-secondary m-auto mb-2"
                  @click="upvote(marker.muid)"
                >
                  <font-awesome-icon
                    icon="fa-solid fa-thumbs-up"
                    class="text-accent mr-2"
                    size="2x"
                  />
                  <span class="font-bold">{{ marker.upvotes }}</span>
                </button>
              </CustomControl>
              <div v-if="marker.photoUrls.length > 0" class="flex flex-row">
                <div class="flex flex-wrap -m-1 md:-m-2">
                  <div
                    class="flex flex-wrap w-1/3"
                    v-for="(url, i) in marker.photoUrls"
                    :key="i"
                  >
                    <div class="w-full p-1 md:p-2">
                      <img
                        alt="gallery"
                        class="block object-cover object-center w-full h-full rounded-lg"
                        :src="url"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div></div>
        </InfoWindow>
      </Marker>
    </MarkerCluster>
  </GoogleMap>
</template>

<script>
import { defineComponent } from "vue";
import { mapStores, mapActions } from "pinia";
import useMapMarkersStore from "@/stores/mapMarkers";
import { GoogleMap, Marker, InfoWindow } from "vue3-google-map";

export default defineComponent({
  components: { GoogleMap, Marker, InfoWindow },

  data() {
    return {
      apikey: import.meta.env.VITE_GMAPS_API_KEY,
      center: {},
      markers: [],
      styles: [
        {
          featureType: "all",
          elementType: "labels.text.fill",
          stylers: [
            {
              color: "#ffffff",
            },
          ],
        },
        {
          featureType: "all",
          elementType: "labels.text.stroke",
          stylers: [
            {
              visibility: "on",
            },
            {
              color: "#3e606f",
            },
            {
              weight: 2,
            },
            {
              gamma: 0.84,
            },
            {
              lightness: "0",
            },
          ],
        },
        {
          featureType: "all",
          elementType: "labels.icon",
          stylers: [
            {
              visibility: "off",
            },
          ],
        },
        {
          featureType: "administrative",
          elementType: "geometry",
          stylers: [
            {
              weight: 0.6,
            },
            {
              color: "#1a3541",
            },
          ],
        },
        {
          featureType: "landscape",
          elementType: "geometry",
          stylers: [
            {
              color: "#2c5a71",
            },
          ],
        },
        {
          featureType: "landscape.man_made",
          elementType: "geometry",
          stylers: [
            {
              visibility: "on",
            },
            {
              hue: "#00abff",
            },
            {
              lightness: "-32",
            },
            {
              weight: "4",
            },
            {
              gamma: "1.27",
            },
          ],
        },
        {
          featureType: "landscape.man_made",
          elementType: "geometry.stroke",
          stylers: [
            {
              hue: "#00a4ff",
            },
            {
              visibility: "on",
            },
            {
              lightness: "-53",
            },
            {
              gamma: "0.69",
            },
            {
              saturation: "13",
            },
          ],
        },
        {
          featureType: "landscape.man_made",
          elementType: "labels.text.fill",
          stylers: [
            {
              visibility: "off",
            },
            {
              hue: "#ff0000",
            },
          ],
        },
        {
          featureType: "poi",
          elementType: "geometry",
          stylers: [
            {
              color: "#406d80",
            },
          ],
        },
        {
          featureType: "poi.park",
          elementType: "geometry",
          stylers: [
            {
              color: "#2c5a71",
            },
          ],
        },
        {
          featureType: "road",
          elementType: "geometry",
          stylers: [
            {
              color: "#29768a",
            },
            {
              lightness: -37,
            },
          ],
        },
        {
          featureType: "transit",
          elementType: "geometry",
          stylers: [
            {
              color: "#406d80",
            },
          ],
        },
        {
          featureType: "water",
          elementType: "geometry",
          stylers: [
            {
              color: "#193341",
            },
          ],
        },
      ],
    };
  },
  computed: {
    ...mapStores(useMapMarkersStore),
  },
  methods: {
    ...mapActions(useMapMarkersStore, ["getMarkers", "upvoteMarker"]),
    async updateMarkers() {
      await this.getMarkers();
      this.markers = this.mapMarkersStore.markers;
    },
    async upvote(muid) {
      await this.upvoteMarker(muid);
      this.updateMarkers();
    },
  },
  mounted() {
    this.updateMarkers();
    this.center = this.mapMarkersStore.center;
  },
});
</script>
