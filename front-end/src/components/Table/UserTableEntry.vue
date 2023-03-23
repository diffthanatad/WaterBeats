<template>
    <tr>
        <td>{{ item.name }}</td>
        <td>{{ item.username }}</td>
        <td>{{ item.role }}</td>
        <td>{{ item.disable ? "Deactivated" : "Active" }}</td>
        <td>
            <button type="button" class="btn btn-warning" style="margin-right: 10px;" @click.prevent="showUpdateUserModal" :disabled="isYourself">
                <i class="bi bi-pencil-square"></i>
            </button>
            <button type="button" class="btn btn-danger" @click.prevent="showDeleteUserModal" :disabled="isYourself">
                <i class="bi bi-trash"></i>
            </button>
        </td>
        <confirm-dialogue ref="confirmDialogue"></confirm-dialogue>
        <update-user-dialogue ref="updateUserDialogue"></update-user-dialogue>
    </tr>
</template>
  
<script>
import ConfirmDialogue from "@/components/Modal/ConfirmDialogue.vue";
import UpdateUserDialogue from "@/components/Modal/UpdateUserDialogue.vue";
import { deleteUser } from "@/services/userService.js";

export default {
    name: "UserTableEntry",
    props: {
        item: Object,
    },
    components: {
        ConfirmDialogue,
        UpdateUserDialogue,
    },
    computed: {
        isYourself() {
            const USERNAME = localStorage.getItem('username');
            return USERNAME === this.$props.item.username;
        }
    },
    methods: {
        async showUpdateUserModal() {
            try {
                const ok = await this.$refs.updateUserDialogue.show({
                    title: 'Update User',
                    okButton: 'yes',
                    name: this.$props.item.name,
                    username: this.$props.item.username,
                    role: this.$props.item.role,
                    status: this.$props.item.disable ? 1 : 0,
                    id: this.$props.item.id,
                });

                if (ok) {
                    this.$emit('refreshPage')
                }
            } catch (error) {
                console.log("UserTableEntry, showUpdateUserModal():", error, "\n");
            }
        },
        async showDeleteUserModal() {
            try {
                const ok = await this.$refs.confirmDialogue.show({
                    title: 'Delete user',
                    message: 'Do you want to delete this user?',
                    okButton: 'yes',
                });

                if (ok) {
                    await deleteUser(this.$props.item.id)
                    this.$emit('refreshPage')
                }
            } catch (error) {
                console.log("UserTableEntry, showDeleteUserModal():", error, "\n");
            }
        },
    }
}
</script>
  
<style scoped></style>