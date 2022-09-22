<template>
  <div class="container flex flex-start">
    <GMapMap
      :center="center"
      :zoom="13"
      map-type-id="terrain"
      style="width: 100vw; height: 50vh"
    >
      <GMapCluster>
        <GMapMarker
          :key="index"
          v-for="(m, index) in markers"
          :position="m.position"
          :clickable="true"
          :draggable="true"
          @click="center = m.position"
        />
      </GMapCluster>
    </GMapMap>
  </div>
</template>

<script>
export default {
  name: "appExplore",
  data() {
    return {
      center: { lat: -20.1609, lng: 57.5012 },
      markers: [
        {
          position: {
            lat: 51.093048,
            lng: 6.84212,
          },
        }, // Along list of clusters
      ],
    };
  },
};
</script>
