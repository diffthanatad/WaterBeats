<template>
    <div>
        <l-map :center="center" :zoom="zoom" class="map" ref="map" @update:zoom="zoomUpdated"
            @update:center="centerUpdated" style="width: 100%">
            <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
            <map-marker v-for="device in devices" :key="device.id" :marker="device"></map-marker>
        </l-map>
    </div>
</template>
  
<script>
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";

import MapMarker from '@/components/Map/MapMarker.vue'

export default {
    name: "MapComponent",
    props: {
        inputDevices: {
            type: Array,
            required: true
        }
    },
    components: {
        LMap,
        LTileLayer,
        MapMarker,
    },
    data() {
        return {
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            center: [51.52498676710948, -0.1344647153442085], /* University College London */
            attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            zoom: 16,
            interval: 7,
            devices: this.inputDevices,
        };
    },
    methods: {
        zoomUpdated(zoom) {
            this.zoom = zoom;
        },
        centerUpdated(center) {
            this.center = center;
        },
    }
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