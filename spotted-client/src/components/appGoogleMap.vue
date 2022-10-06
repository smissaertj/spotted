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
        <InfoWindow class="text-accent-content w-fit">
          <div>
            <h1 class="font-bold text-4xl m-2">{{ marker.title }}</h1>
            <div>
              <p class="text-2xl m-2">
                <span class="font-bold">Category:</span> {{ marker.category }}
              </p>
              <p class="text-2xl m-2">
                {{ marker.desc }}
              </p>
            </div>
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
      styles: [],
    };
  },
  computed: {
    ...mapStores(useMapMarkersStore),
  },
  methods: {
    ...mapActions(useMapMarkersStore, ["getMarkers"]),
    async updateMarkers() {
      await this.getMarkers();
      this.markers = this.mapMarkersStore.markers;
    },
  },
  mounted() {
    this.updateMarkers();
    this.center = this.mapMarkersStore.center;
  },
});
</script>
