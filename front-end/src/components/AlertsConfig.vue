<template>
<div class="container">
  <div class="alert-box">
    <div>
      <label style="color: #f7646c">Temperature</label>
    </div>
    <div class="img-input">
      <img class="temp-img" src=".././assets/img/temperature.jpeg">
      <input class="sensor-value" value="16 C°">
    </div>
  </div>
  <div class="alert-box">
    <div>
      <label style="color: #01286f">Soil Moisture</label>
    </div>
    <div class="img-input">
      <img class="moisture-img" src=".././assets/img/soil_moisture.png">
      <input class="sensor-value" value="24%">
    </div>
  </div>
  <div class="alert-box">
    <div>
      <label style="color: #65a2fe">Water Level</label>
    </div>
    <div class="img-input">
      <img class="water-lvl-img" src=".././assets/img/water_level.png">
      <input class="sensor-value" value="10 MM">
    </div>
  </div>
  <div class="alert-box">
    <div>
      <label style="color: #2deca4">Water Pollution</label>
    </div>
    <div class="img-input">
      <img class="pollution-img" src=".././assets/img/water_pollution.png">
      <input class="sensor-value" value="23 ppm">
    </div>
  </div>
</div>
</template>


<script>
export default {
  name: 'AlertsConfig',
  data() {
    return {
      alertBox : []
    }
  },
  methods: {
    fillAlertBox() {
      const sensorName = ["Temperature", "Soil Moisture", "Water Level", "Water Pollution"]
      const imgLoc = [
        ".././assets/img/temperature.jpeg",
        ".././assets/img/soil_moisture.png",
        ".././assets/img/water_level.png",
        ".././assets/img/water_pollution.png"
      ]
      const defaultVal = ["18", "67", "", ""]
      const units = ["C°", "%", "", ""]

      for (let i in Array.from(Array(4).keys())) {
        this.alertBox.push({
          sensorName: sensorName[i],
          imgLoc: imgLoc[i],
          defaultVal: defaultVal[i],
          units: units[i]
        })
      }
    }
  },
  created() {
    this.fillAlertBox()
  }
}
</script>


<style scoped>

label {
  font-size: 30px;
  padding-left: 20px;
  padding-top: 2px;
}

input {
  border-radius: 50px;
  width: 80px;
  height: 80px;
  outline: 0 none;
  text-align: center;
  outline-color: transparent;
  font-size: 20px;
}

.img-input {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  padding-top: 25px;
}

.alert-box {
  border-radius: 25px;
  border: 2px solid #888888;
  box-shadow: 5px 10px #888888;
  width: 270px;
  height: 270px;
}

.container {
  display: flex;
  gap: 70px;
}
.temp-img {
  width: 6vw;
}

.moisture-img {
  width: 9vw;
}

.water-lvl-img {
  width: 10vw;
}

.pollution-img {
  width: 10.5vw;
}

</style>