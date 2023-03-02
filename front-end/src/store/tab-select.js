import {ref} from "vue";

export const tabSelect = ref({
    tabNames: ["temperature", "moisture", "pollution_level", "water_level"],
    selectedTab: "temperature",
    setSelectedTab(name) {
        this.selectedTab = name
    }
});