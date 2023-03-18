<template>
    <div class="configuration-page">
        <div class="left-half">
            <MapComp />
        </div>
        <div class="right-half">
            <h3 style="padding-top: 10px;">Actuator Rules Page</h3>
            <hr />
            <div class="graph-tab d-flex justify-content-center">
                <div class="tab">
                    <button v-for="tab in tabNames" :key="tab" :style="tabColor(tab)" @click="updateSelected(tab)">
                        {{ tab }}
                    </button>
                </div>
            </div>
            <br>
            <div v-if='switchTabs' class='tab1'>
                <div class="container">
                    <FormRuleSetting />
                </div>
            </div>
            <div v-if='!switchTabs' class='tab2'>
                <RulesTable />
            </div>
        </div>
    </div>
</template>

<script>
import MapComp from '@/components/Map/MapComp.vue'
import FormRuleSetting from '@/components/Form/FormRuleSetting.vue';
import RulesTable from '@/components/Table/RulesTable.vue';
import { getRuleByActuatorId } from '@/services/ruleService.js';
import { getLatestReadingForAllDevices } from "@/services/deviceService.js";
import moment from 'moment';

export default {
    name: 'ActuatorConfigurationView',
    components: {
        MapComp,
        FormRuleSetting,
        RulesTable
    },
    data() {
        return {
            tabNames: ['ADD RULE', 'EXISTING RULES'],
            switchTabs: true,
            selectedTab: 'ADD RULE',
            rules: {
                temperatureLow: "1",
                temperatureHigh: "2",
                soilMoistureLow: "3",
                soilMoistureHigh: "4",
                minute: "10",
                time: "10:00",
            },
        };
    },
    mounted() {
        this.getAllDevices()
    },
    methods: {
        async getAllDevices() {
            try {
                const response = await getLatestReadingForAllDevices();

                if (response.status === 200) {
                    var DEVICES = response.data.data;

                    DEVICES.forEach(element => {
                        element.timestamp = moment(element.time).format('Do MMMM YYYY, h:mm:ss a');
                        var temp = Number(element.data);
                        if (temp) { element.value = `${temp.toFixed(2)} ${element.unit}`; }
                        else { element.value = "" }
                    });

                    this.$store.dispatch("device/update", DEVICES);
                }
            } catch (error) {
                console.log("HomeView.vue, getAllDevices():", error);
            }
        },
        async getRuleByActuatorId() {
            try {
                console.log("getRuleByActuatorId():", this.selectedDevice)
                this.rules = {}

                const response = await getRuleByActuatorId(this.selectedDevice);

                if (response.status !== 200) { return; }

                const data = response.data;
                this.rules = data;
            } catch (error) {
                console.log("ActuatorConfigurationView.vue, getRuleByActuatorId():", error);
            }
        },
        tabColor(tabName) {
            let color = (this.selectedTab === tabName) ? "#5cbcac" : "#3fd9b3"
            return 'background-color: ' + color + ';'
        },
        updateSelected(tabName) {
            if (tabName != this.selectedTab) {
                this.selectedTab = tabName
                this.switchTabs = !this.switchTabs
            }
        }
    },
    created() {
        this.selectedTab = this.tabNames[0]
    }
}
</script>

<style scoped>
h3 {
    text-align: center;
    padding-top: 30px;
}

ActuatorSetting {
    padding-bottom: 20px;
}

.configuration-page {
    height: 100%;
}

.btn {
    width: 100px;
}

.bi {
    margin-right: 5px;
}

.left-half {
    position: absolute;
    left: 0px;
    width: 55%;
    height: 93.5%;
}

.right-half {
    position: absolute;
    right: 0px;
    width: 45%;
    padding: 10px 20px;
}

.tab {
    display: flex;
    align-items: center;
    justify-content: space-evenly;
    background-color: #3fd9b3;
    overflow: hidden;
    width: 100%;
    height: 30px;
    border: none;
    font-size: 13px;
}

.tab button {
    display: flex;
    border: 1px solid #fff;
    cursor: pointer;
    padding: 14px 16px;
    color: #fff;
    width: 100%;
    justify-content: center;
}
</style>
