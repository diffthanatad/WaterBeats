<template>
    <div>
        <l-map :center="center" :zoom="zoom" class="map" ref="map" @update:zoom="zoomUpdated" @update:center="centerUpdated"
            style="width: 100%">
            <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
            <map-marker v-for="item in device.devices" :key="item.id" :marker="item"></map-marker>
        </l-map>
    </div>
</template>
  
<script>
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";

import { mapState } from "vuex";
import MapMarker from '@/components/Map/MapMarker.vue'

export default {
    name: "MapComponent",
    props: {
    },
    components: {
        LMap,
        LTileLayer,
        MapMarker,
    },
    data() {
        return {
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            center: [55.168784332733914, -2.413875061176684], /* Ferny Rigg Alpacas */
            attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            zoom: 19,
            interval: 7,
            devices: [],
        };
    },
    mounted() {
        this.loadDevice();
    },
    computed: {
        ...mapState(['device']),
    },
    methods: {
        loadDevice() {
            this.devices = this.$store.getters['device/getDevices'];
        },
        zoomUpdated(zoom) {
            this.zoom = zoom;
        },
        centerUpdated(center) {
            this.center = center;
        },
    },
};
</script>
  
<style>
.map {
    position: absolute;
    width: 100%;
    height: 100%;
    overflow: hidden
}
</style>