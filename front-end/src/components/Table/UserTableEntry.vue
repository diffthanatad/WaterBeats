<template>
    <tr>
        <td>{{ item.name }}</td>
        <td>{{ item.username }}</td>
        <td>{{ item.role }}</td>
        <td>{{ item.status ? "Active" : "Deactivated" }}</td>
        <td>
            <button type="button" class="btn btn-warning" style="margin-right: 10px;" @click.prevent="showUpdateUserModal">
                <i class="bi bi-pencil-square"></i>
            </button>
            <button type="button" class="btn btn-danger" @click.prevent="showDeleteUserModal">
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
// import { deleteUser, updateUser } from "@/services/userService.js";

export default {
    name: "UserTableEntry",
    props: {
        item: Object,
    },
    components: {
        ConfirmDialogue,
        UpdateUserDialogue,
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
                    status: this.$props.item.status,
                    id: this.$props.item.id,
                });

                if (ok) {
                    this.$emit('refreshPage')
                }
            } catch (error) {
                console.log("error:", error);
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
                    // await deleteUser(this.$props.item.id)
                    this.$emit('refreshPage')
                }
            } catch (error) {
                console.log("error:", error);
            }
        },
    }
}
</script>
  
<style scoped></style>