<template>
    <div class="configuration-page">
        <div class="left-half">
            <MapComp :inputDevices="devices" />
        </div>
        <div class="right-half">
            <h1>Actuator Configuration Page</h1>
            <hr />
            <div class="row mb-3">
                <div class="col-6">
                    <select class="form-select" name="field" as="select" v-model="deviceType">
                        <option value="pump">Pump</option>
                        <option value="sprinkler">Sprinkler</option>
                    </select>
                </div>
                <div class="col-6">
                    <button type="button" class="btn btn-primary col-6" @click.prevent="getActuatorByType">
                        <i class="bi bi-search"></i>Search
                    </button>
                </div>
            </div>
            <div class="input-group mb-3">
                <label class="input-group-text" for="inputGroupSelect01">Currently Selected Device</label>
                <select class="form-select" id="inputGroupSelect01" v-model="selectedDevice">
                    <option v-for="device in devices" :key="device.id" :value="device.id"> {{ device.id }} </option>
                </select>
            </div>
            <hr />
            <h3> Rules </h3>
            <form @submit.prevent="onSubmitRule">
                <div class="row mb-3">
                    <FormRuleSetting label="Turn on when temperature is" firstInputLabel="Low"
                        firstPlaceholder="low ..." :firstInputInitialValue="rules.temperatureLow"
                        secondInputLabel="High" secondPlaceholder="high ..."
                        :secondInputInitialValue="rules.temperatureHigh"
                        @onChangeInputValue="changeInputValueForTemperature" />
                </div>
                <div class="row mb-3">
                    <FormRuleSetting label="Turn on when soil moisture is" firstInputLabel="Low"
                        firstPlaceholder="low ..." :firstInputInitialValue="rules.soilMoistureLow"
                        secondInputLabel="High" secondPlaceholder="high ..."
                        :secondInputInitialValue="rules.soilMoistureHigh"
                        @onChangeInputValue="changeInputValueForSoilMoisture" />
                </div>
                <div class="row mb-3">
                    <FormRuleSetting label="Turn on when time is" firstInputLabel="Min" firstPlaceholder="minutes?"
                        :firstInputInitialValue="rules.minute" secondInputLabel="Time" secondPlaceholder=" 24 hr."
                        :secondInputInitialValue="rules.time" @onChangeInputValue="changeInputValueForTime" />
                </div>
                <div class="row justify-content-center">
                    <button class="btn btn-primary"><i class="bi bi-save2"></i>Save</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import MapComp from '@/components/Map/MapComp.vue'
import FormRuleSetting from '@/components/Form/FormRuleSetting.vue';
import { getActuatorByType } from '@/services/actuatorService.js';
import { getRuleByActuatorId, updateRuleByActuatorId } from '@/services/ruleService.js';

// import { Form } from 'vee-validate';

export default {
    name: 'ActuatorConfigurationView',
    components: {
        // Form,
        MapComp,
        FormRuleSetting,
    },
    data() {
        return {
            selectedDevice: '',
            deviceType: 'pump',
            devices: [
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
                }
            ],
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
        // this.getActuatorByType();
    },
    methods: {
        async getActuatorByType() {
            try {
                console.log("getActuatorByType():", this.deviceType)

                this.actuators.length = 0;
                const response = await getActuatorByType(this.deviceType);

                if (response.status !== 200) { return; }

                const data = response.data;
                this.actuators = data;
            } catch (error) {
                console.log("ActuatorConfigurationView.vue, getActuatorByType():", error);
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
        async onSubmitRule() {
            try {
                const obj = {
                    temperature_low: this.rules.temperatureLow,
                    temperature_high: this.rules.temperatureHigh,
                    soil_moisture_low: this.rules.soilMoistureLow,
                    soil_moisture_high: this.rules.soilMoistureHigh,
                    time_period: this.rules.minute,
                    start_time: this.rules.time,
                }
                console.log("onSubmitRule():", obj);
                await updateRuleByActuatorId(obj);
            } catch (error) {
                console.log("ActuatorConfigurationView.vue, onSubmitRule():", error);
            }
        },
        changeInputValueForTemperature(obj) {
            this.rules.temperatureLow = obj.firstInputValue;
            this.rules.temperatureHigh = obj.secondInputValue;
        },
        changeInputValueForSoilMoisture(obj) {
            this.rules.soilMoistureLow = obj.firstInputValue;
            this.rules.soilMoistureHigh = obj.secondInputValue;
        },
        changeInputValueForTime(obj) {
            this.rules.minute = obj.firstInputValue;
            this.rules.time = obj.secondInputValue;
        },
    },
    watch: {
        selectedDevice() {
            // this.getRuleByActuatorId();
        }
    },
}
</script>

<style scoped>
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
    width: 50%;
    height: 93.5%;
}

.right-half {
    position: absolute;
    right: 0px;
    width: 50%;
    padding: 10px 20px;
}
</style>>
