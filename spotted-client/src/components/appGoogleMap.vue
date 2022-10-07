<template>
  <GoogleMap
    :api-key="apikey"
    :center="center"
    :zoom="11"
    zoom-control-position="TOP_RIGHT"
    :disable-default-ui="true"
    :styles="styles"
    class="w-full h-1/2"
    @click="$emit('addMarker', $event)"
  >
    <MarkerCluster>
      <template v-for="(marker, i) in markers" :key="i">
        <Marker
          v-if="marker.isVisible"
          :options="{
            position: marker.position,
            label: marker.label,
            title: marker.title,
            clickable: marker.clickable,
          }"
        >
          <InfoWindow class="text-accent-content w-fit glass">
            <div class="mockup-window bg-base-200/25">
              <div class="flex flex-col justify-center px-4 py-4 bg-base-100">
                <h1 class="font-bold text-accent text-4xl m-2">
                  {{ marker.title }}
                </h1>
                <div
                  class="badge badge-lg badge-primary text-2xl m-2 font-bold"
                >
                  {{ marker.authority }}
                </div>
                <p class="text-2xl text-white">
                  {{ marker.desc }}
                </p>
                <CustomControl position="CENTER">
                  <button
                    class="btn btn-block btn-secondary m-auto mb-2"
                    @click="downvote(marker.muid)"
                  >
                    <font-awesome-icon
                      icon="fa-solid fa-thumbs-down"
                      class="text-accent mr-2"
                      size="2x"
                    />
                    <span class="font-bold text-2xl text-white">{{
                      marker.downvotes
                    }}</span>
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
          </InfoWindow>
        </Marker>
      </template>
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
          elementType: "labels.text",
          stylers: [
            {
              color: "#a1f7ff",
            },
          ],
        },
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
              color: "#000000",
            },
            {
              lightness: 13,
            },
          ],
        },
        {
          featureType: "administrative",
          elementType: "geometry.fill",
          stylers: [
            {
              color: "#000000",
            },
          ],
        },
        {
          featureType: "administrative",
          elementType: "geometry.stroke",
          stylers: [
            {
              color: "#144b53",
            },
            {
              lightness: 14,
            },
            {
              weight: 1.4,
            },
          ],
        },
        {
          featureType: "administrative",
          elementType: "labels.text",
          stylers: [
            {
              visibility: "simplified",
            },
            {
              color: "#a1f7ff",
            },
          ],
        },
        {
          featureType: "administrative.province",
          elementType: "labels.text",
          stylers: [
            {
              visibility: "simplified",
            },
            {
              color: "#a1f7ff",
            },
          ],
        },
        {
          featureType: "administrative.locality",
          elementType: "labels.text",
          stylers: [
            {
              visibility: "simplified",
            },
            {
              color: "#a1f7ff",
            },
          ],
        },
        {
          featureType: "administrative.neighborhood",
          elementType: "labels.text",
          stylers: [
            {
              visibility: "simplified",
            },
            {
              color: "#a1f7ff",
            },
          ],
        },
        {
          featureType: "landscape",
          elementType: "all",
          stylers: [
            {
              color: "#08304b",
            },
          ],
        },
        {
          featureType: "poi",
          elementType: "geometry",
          stylers: [
            {
              color: "#0c4152",
            },
            {
              lightness: 5,
            },
          ],
        },
        {
          featureType: "poi.attraction",
          elementType: "labels",
          stylers: [
            {
              invert_lightness: true,
            },
          ],
        },
        {
          featureType: "poi.attraction",
          elementType: "labels.text",
          stylers: [
            {
              visibility: "simplified",
            },
            {
              color: "#a1f7ff",
            },
          ],
        },
        {
          featureType: "poi.park",
          elementType: "labels",
          stylers: [
            {
              visibility: "on",
            },
            {
              invert_lightness: true,
            },
          ],
        },
        {
          featureType: "poi.park",
          elementType: "labels.text",
          stylers: [
            {
              visibility: "simplified",
            },
            {
              color: "#a1f7ff",
            },
          ],
        },
        {
          featureType: "road",
          elementType: "labels.text",
          stylers: [
            {
              color: "#a1f7ff",
            },
          ],
        },
        {
          featureType: "road.highway",
          elementType: "geometry.fill",
          stylers: [
            {
              color: "#000000",
            },
          ],
        },
        {
          featureType: "road.highway",
          elementType: "geometry.stroke",
          stylers: [
            {
              color: "#0b434f",
            },
            {
              lightness: 25,
            },
          ],
        },
        {
          featureType: "road.highway",
          elementType: "labels",
          stylers: [
            {
              lightness: "0",
            },
            {
              saturation: "0",
            },
            {
              invert_lightness: true,
            },
            {
              visibility: "off",
            },
            {
              hue: "#00e9ff",
            },
          ],
        },
        {
          featureType: "road.highway",
          elementType: "labels.text",
          stylers: [
            {
              visibility: "simplified",
            },
            {
              color: "#a1f7ff",
            },
          ],
        },
        {
          featureType: "road.highway.controlled_access",
          elementType: "labels.text",
          stylers: [
            {
              color: "#a1f7ff",
            },
          ],
        },
        {
          featureType: "road.arterial",
          elementType: "geometry.fill",
          stylers: [
            {
              color: "#000000",
            },
          ],
        },
        {
          featureType: "road.arterial",
          elementType: "geometry.stroke",
          stylers: [
            {
              color: "#0b3d51",
            },
            {
              lightness: 16,
            },
          ],
        },
        {
          featureType: "road.arterial",
          elementType: "labels",
          stylers: [
            { visibility: "off" },
            {
              invert_lightness: true,
            },
          ],
        },
        {
          featureType: "road.local",
          elementType: "geometry",
          stylers: [
            {
              color: "#000000",
            },
          ],
        },
        {
          featureType: "road.local",
          elementType: "labels",
          stylers: [
            {
              visibility: "off",
            },
            {
              invert_lightness: true,
            },
          ],
        },
        {
          featureType: "transit",
          elementType: "all",
          stylers: [
            {
              color: "#146474",
            },
          ],
        },
        {
          featureType: "water",
          elementType: "all",
          stylers: [
            {
              color: "#021019",
            },
          ],
        },
      ],
    };
  },
  computed: {
    ...mapStores(useMapMarkersStore),
    markers: function () {
      return this.mapMarkersStore.markers.filter((i) => i.isVisible === true);
    },
  },
  methods: {
    ...mapActions(useMapMarkersStore, ["getMarkers", "downvoteMarker"]),
    async updateMarkers() {
      await this.getMarkers();
      this.markers = this.mapMarkersStore.markers;
    },
    async downvote(muid) {
      await this.downvoteMarker(muid);
      this.updateMarkers();
    },
  },
  mounted() {
    this.updateMarkers();
    this.center = this.mapMarkersStore.center;
  },
});
</script>
