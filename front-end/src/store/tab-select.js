import {ref} from "vue";

export const tabSelect = ref({
    tabNames: ["TEMPERATURE", "MOISTURE", "POLLUTION LEVEL", "WATER LEVEL"],
    selectedTab: "TEMPERATURE",
    setSelectedTab(name) {
        this.selectedTab = name
    }
});