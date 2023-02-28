<template>
  <popup-modal ref="popup">
    <h2 style="margin-top: 0">{{ title }}</h2>
    <div class="row mb-3">
      <label for="usernameInput" class="col-4 col-form-label">Username</label>
      <div class="col-8">
        <input type="text" class="form-control" id="usernameInput" v-model="username">
      </div>
    </div>
    <div class="row mb-3">
      <label for="nameInput" class="col-4 col-form-label">Full name</label>
      <div class="col-8">
        <input type="text" class="form-control" id="nameInput" v-model="name">
      </div>
    </div>
    <div class="row mb-3">
      <label for="roleInput" class="col-4 col-form-label">Role </label>
      <div class="col-8">
        <select class="form-select" aria-label="Default select example" id="roleInput" v-model="role">
          <option value="admin">admin</option>
          <option value="moderator">moderator</option>
          <option value="user">user</option>
        </select>
      </div>
    </div>
    <div class="row mb-3">
      <label for="statusInput" class="col-4 col-form-label">Status </label>
      <div class="col-8">
        <select class="form-select" aria-label="Default select example" id="statusInput" v-model="status">
          <option value="1">active</option>
          <option value="0">deactivated</option>
        </select>
      </div>
    </div>
    
    <div class="btns">
      <button class="cancel-btn" @click="_cancel">{{ cancelButton }}</button>
      <button class="ok-btn" @click="_confirm">{{ okButton }}</button>
    </div>
  </popup-modal>
</template>

<script>
import PopupModal from '@/components/Modal/PopupModal.vue';
import { updateUser } from "@/services/userService.js";

export default {
  name: 'UpdateUserDialogue',
  components: { PopupModal },
  data: () => ({
    /* Parameters that change depending on the type of dialogue. */
    title: undefined,
    message: undefined, /* Main text content. */
    okButton: undefined, /* Text for confirm button; leave it empty because we don't know what we're using it for. */
    cancelButton: 'No', /* Text for cancel button. */
    username: undefined,
    name: undefined,
    role: undefined,
    status: undefined,
    id: undefined,

    /* Private variables. */
    resolvePromise: undefined,
    rejectPromise: undefined,
  }),
  methods: {
    show(opts = {}) {
      this.title = opts.title
      this.message = opts.message
      this.okButton = opts.okButton

      this.username = opts.username;
      this.name = opts.name;
      this.role = opts.role;
      this.status = opts.status;
      this.id = opts.id;

      if (opts.cancelButton) {
        this.cancelButton = opts.cancelButton
      }
      // Once we set our config, we tell the popup modal to open
      this.$refs.popup.open()
      // Return promise so the caller can get results
      return new Promise((resolve, reject) => {
        this.resolvePromise = resolve
        this.rejectPromise = reject
      })
    },
    async _confirm() {
      const obj = {
        id: this.id,
        username: this.username,
        name: this.name,
        role: this.role,
        status: this.status,
      };

      const response = await updateUser(obj);

      if (response.status === 201) {
        this.$refs.popup.close()
        this.resolvePromise(true)
      }
    },
    _cancel() {
      this.$refs.popup.close()
      this.resolvePromise(false)
      // Or you can throw an error
      // this.rejectPromise(new Error('User cancelled the dialogue'))
    },
  },
}
</script>

<style scoped>
.btns {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.cancel-btn {
  padding: 0.5em 1em;
  background-color: #eccfc9;
  color: #c5391a;
  border: 2px solid #ea3f1b;
  border-radius: 5px;
  font-weight: bold;
  font-size: 16px;
  text-transform: uppercase;
  cursor: pointer;
}

.ok-btn {
  padding: 0.5em 1em;
  background-color: #d5eae7;
  color: #35907f;
  border: 2px solid #0ec5a4;
  border-radius: 5px;
  font-weight: bold;
  font-size: 16px;
  text-transform: uppercase;
  cursor: pointer;
}
</style>