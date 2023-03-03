<template>
  <div class="setting">
    <div class="user-detail container">
      <h1>User Detail</h1>
      <div class="user-detail-box container">
        <div class="column-user-detail">
          <label><b>Username: </b></label>
        </div>
        <div class="column-user-detail">
          <label> {{ username }}</label>
        </div>
        <div class="column-user-detail">
          <label><b>Full Name: </b></label>
        </div>
        <div class="column-user-detail">
          <label> {{ fullname }}</label>
        </div>
        <div class="column-user-detail">
          <label><b>Role: </b></label>
        </div>
        <div class="column-user-detail">
          <label> {{ role }}</label>
        </div>
      </div>
    </div>
    <div class="change-password container">
      <h1>Change Password</h1>
      <div class="change-password-box container">
        <form>
          <div class="form-row">
            <label>Current Password: </label>
            <input
              v-model="currentPassword"
              type="password"
              placeholder="Current Password"
            />
            <br />
          </div>
          <div class="form-row">
            <label>New Password: </label>
            <input
              v-model="newPassword"
              type="password"
              placeholder="New Password"
            />
            <br />
          </div>
          <div class="form-row">
            <label>Confirm New Password: </label>
            <input
              v-model="confirmNewPassword"
              type="password"
              placeholder="Confirm New Password"
            />
            <br />
          </div>
          <button @click.prevent="changePasswordFunc">Change Password</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getSingleUser, changePassword } from "@/services/userService";

export default {
  name: "SettingView",
  components: {},
  data() {
    return {
      username: "",
      fullname: "",
      role: "",
      id: 0,
      currentPassword: "",
      newPassword: "",
      confirmNewPassword: "",
    };
  },
  async mounted() {
    await this.getUserData();
  },
  methods: {
    async changePasswordFunc() {
      if (this.newPassword === this.confirmNewPassword) {
        const jsonData = {
          id: this.id,
          oldPassword: this.currentPassword,
          newPassword: this.newPassword,
        };
        const response = await changePassword(jsonData);
        if (response.status === 200) {
          alert("Change password successfully");
        } else {
          alert("Change password failed");
        }
      }
    },
    async getUserData() {
      this.username = localStorage.getItem("username");
      const response = await getSingleUser(this.username);
      this.fullname = response.data.name;
      this.role = response.data.role;
      this.id = response.data.id;
    },
  },
};
</script>
<style scoped>
.user-detail {
  display: box;
  margin-top: 20px;
  outline-style: solid;
  height: 150px;
}
.user-detail-box {
  align-items: center;
  display: box;
  flex-direction: column;
  justify-content: center;
  padding-left: 25%;
  width: 100%;
}

.column-user-detail {
  float: left;
  width: 50%;
}

.change-password {
  margin-top: 10px;
  outline-color: black;
  outline-style: solid;
}

.change-password-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.column {
  float: left;
  width: 50%;
  /* box-sizing: border-box;
  padding: 0 20px; */
}

input {
  margin: 0 auto;
}

.form-row {
  display: grid;
  grid-template-columns: min-content 1fr;
  grid-gap: 10px;
}

label {
  text-align: left;
}

input,
textarea {
  width: 100%;
  box-sizing: border-box;
}

button {
  margin: 0 auto;
  margin-top: 10px;
  width: 100%;
  background-color: #4caf50;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>