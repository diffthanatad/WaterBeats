<template>
  <div class="admin container">
    <h1>Admin Configuration Page</h1>
    <div class="d-flex mb-3">
      <div class="p-2">
        <div class="form-group row justify-content-center">
          <label for="usernameInput" class="col-4 col-form-label">Username</label>
          <div class="col-8">
            <input type="text" class="form-control" id="usernameInput" placeholder="username..." v-model="searchUsername"
              @keyup.enter="getAllUsers" />
          </div>
        </div>
      </div>
      <div class="p-2">
        <button type="button" class="btn btn-primary" @click.prevent="getAllUsers">
          <span><i class="bi bi-search" style="margin-right: 5px;"></i>search</span>
        </button>
      </div>
      <div class="ms-auto p-2">
        <button type="button" class="btn btn-success" @click.prevent="showCreateUserModal"><i
            class="bi bi-person-plus-fill" style="margin-right: 10px;"></i>Create User</button>
      </div>
    </div>
    <hr>
    <div class="navigation-section">
      <pagination-information :currentPage='this.currentPage' :totalPages="totalPages" :totalItems="totalItems"
        :hasPrevious="hasPrevious" :hasNext="hasNext" @clickedChangeCurrentPage="clickedChangeCurrentPage" />
    </div>
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
        <UserTableEntry v-for="user in users" :item="user" :key="user.id" @refreshPage="getAllUsers"></UserTableEntry>
      </transition-group>
    </table>
  </div>
  <create-user-dialogue ref="createUserDialogue"></create-user-dialogue>
</template>

<script>
import UserTableEntry from '@/components/Table/UserTableEntry.vue';
import PaginationInformation from '@/components/Pagination/PaginationInformation.vue';
import CreateUserDialogue from "@/components/Modal/CreateUserDialogue.vue";

import { getAllUsersWithPagination } from "@/services/userService.js";

export default {
  name: 'AdminView',
  components: {
    UserTableEntry,
    PaginationInformation,
    CreateUserDialogue,
  },
  data() {
    return {
      /* Search input field. */
      searchUsername: "",

      /* Data from pagination. */
      hasPrevious: false,
      hasNext: false,
      currentPage: 0,
      totalPages: 0,
      totalItems: 0,
      users: []
    }
  },
  mounted() {
    this.getAllUsers();
  },
  computed: {
  },
  methods: {
    async getAllUsers() {
      const response = await getAllUsersWithPagination(this.searchUsername, this.currentPage);
      this.loadResource(response);
    },
    returnItselfOrDefaultValue(value, defaultValue) {
      if (value) {
        return value;
      } else {
        return defaultValue;
      }
    },
    loadResource(response) {
      this.users = response.data.users;

      this.currentPage = this.returnItselfOrDefaultValue(response.data.currentPage, 0);
      this.totalPages = this.returnItselfOrDefaultValue(response.data.totalPages, 0);
      this.totalItems = this.returnItselfOrDefaultValue(response.data.totalItems, 0);

      this.hasPrevious = this.currentPage <= 0 ? false : true;
      this.hasNext = (this.currentPage + 1) < this.totalPages ? true : false;
    },
    clickedChangeCurrentPage(newCurrentPage) {
      this.currentPage = newCurrentPage;
      this.getAllUsers();
    },
    async showCreateUserModal() {
      try {
        const ok = await this.$refs.createUserDialogue.show({
          title: 'Create User',
          okButton: 'yes',
        });

        if (ok) {
          this.getAllUsers();
          return;
        }
      } catch (error) {
        console.log("error:", error);
      }
    }
  },
  watch: {
  },
}
</script>
