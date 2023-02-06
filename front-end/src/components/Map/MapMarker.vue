<template>
  <div class="marker-component">
    <l-marker :lat-lng="marker.location">
    </l-marker>
  </div>
</template>

<script>
import { LMarker } from '@vue-leaflet/vue-leaflet';

export default {
  name: "MapMarker",
  props: {
    marker: {
      type: Object,
      required: true
    }
  },
  components: { 
    LMarker,
  },
  data() {
    return {
      markerLatLng: [ 51.52397881654594, -0.130105538694122 ],
    }
  },
  computed: {
  },
  mounted() {
  },
  methods: {
  },
  watch: {
  }
}
</script>

<style scoped>
  /* .marker-icon {
    height: 50px;
    width: auto;
  }
  .leaflet-popup-content-wrapper {
    width: 300px;
  }
  .fas {
    margin-right: 10px;
  }
  div {
    font-size: 16px;
  } */
</style>