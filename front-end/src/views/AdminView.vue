<template>
  <div class="admin container">
    <h1>Admin</h1>
    <table id="orderDetail" class="table table-hover table-sm">
      <thead>
        <tr>
          <th style="width:35%;">Fullname</th>
          <th style="width:20%;">Username</th>
          <th style="width:15%;">Role</th>
          <th style="width:15%;">Status</th>
          <th style="width:15%;"></th>
        </tr>
      </thead>
      <transition-group name="list-user" tag="tbody">
        <UserTableEntry v-for="user in users" :item="user" :key="user.id"></UserTableEntry>
      </transition-group>
    </table>
  </div>
</template>

<script>
import UserTableEntry from '@/components/Table/UserTableEntry.vue';

export default {
  name: 'AdminView',
  components: {
    UserTableEntry,
  },
  data() {
    return {
      users: [
        {
          id: 1,
          name: "Adam Smith",
          username: "adam01",
          role: "admin",
          status: 1
        },
        {
          id: 2,
          name: "David Brown",
          username: "david01",
          role: "user",
          status: 0
        },
        {
          id: 3,
          name: "Magnus Carlsen",
          username: "magnus",
          role: "admin",
          status: 1
        },
      ]
    }
  },
  mounted() {
  },
  computed: {
  },
  methods: {
  },
  watch: {
  },
}
</script>
