<template>
    <div>
        <l-map :center="center" :zoom="zoom" class="map" ref="map" @update:zoom="zoomUpdated"
            @update:center="centerUpdated" style="height: 92%; 
            width: 100%">
            <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
            <map-marker v-for="sensor in sensors" :key="sensor.id" :marker="sensor"></map-marker>
        </l-map>
    </div>
</template>
  
<script>
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";

import MapMarker from '@/components/Map/MapMarker.vue'

export default {
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
            sensors: [
                {
                    id: "1",
                    type: "Soil Moisture Sensor",
                    status: "on",
                    value: "0.55 wfv",
                    timestamp: "2023-01-04 18:51:04",
                    location: [51.524692684598826, -0.13405083079203617]
                },
                {
                    id: "2",
                    type: "Soil Moisture Sensor",
                    status: "off",
                    value: null,
                    timestamp: null,
                    location: [51.524926705352485, -0.13249806913374523]
                },
                {
                    id: "3",
                    type: "Temperature Sensor",
                    status: "on",
                    value: "11°C",
                    timestamp: "2023-01-04 16:30:22",
                    location: [51.52191552403864, -0.13179715055845592]
                },
                {
                    id: "4",
                    type: "Temperature Sensor",
                    status: "on",
                    value: "12°C",
                    timestamp: "2023-01-04 15:09:22",
                    location: [51.52597470028996, -0.13253025564190157]
                },
                {
                    id: "5",
                    type: "Water Sprinkler",
                    status: "watering",
                    location: [51.52397881654594, -0.130105538694122]
                },
                {
                    id: "6",
                    type: "Water Sprinkler",
                    status: "off",
                    location: [51.52329792648238, -0.13508371862180735]
                },
                {
                    id: "9",
                    type: "dddWater Sprinkler",
                    status: "off",
                    location: [51.52306410413633, -0.12788555112319272]
                }
            ],
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