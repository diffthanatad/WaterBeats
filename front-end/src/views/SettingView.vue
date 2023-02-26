<template>
  <div class="setting">
    <div class="user-detail">
      <h1>User Detail</h1>
      <div class="col-8">
        <label>Username: {{ username }} </label> <br />
        <label>Full Name: {{ fullname }} </label> <br />
        <label>Role: {{ role }} </label> <br />
        <label>Last Signed In: {{ lastSignedIn }} </label> <br />
      </div>
    </div>
    <div class="change-password">
      <h1>Change Password</h1>
      <div class="col-8">
        <label>Current Password: </label>
        <input
          v-model="currentPassword"
          type="password"
          placeholder="Current Password"
        />
        <br />
        <label>New Password: </label>
        <input
          v-model="newPassword"
          type="password"
          placeholder="New Password"
        />
        <br />
        <label>Confirm New Password: </label>
        <input
          v-model="confirmNewPassword"
          type="password"
          placeholder="Confirm New Password"
        />
        <br />
        <button @click="changePassword">Change Password</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SettingView",
  components: {},
  data() {
    return {
      username: "adam01",
      fullname: "Adam Smith",
      role: "admin",
      lastSignedIn: "2021-05-01 12:00:00",
      currentPassword: "",
      newPassword: "",
      confirmNewPassword: "",
    };
  },
  methods: {
    changePassword() {
      console.log(`${this.currentPassword}-${this.newPassword}-${this.confirmNewPassword}`);
    },
  },
};
</script>
