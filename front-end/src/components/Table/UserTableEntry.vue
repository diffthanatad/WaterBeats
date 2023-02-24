<template>
    <tr>
        <td>{{ item.name }}</td>
        <td>{{ item.username }}</td>
        <td>{{ item.role }}</td>
        <td>{{ item.status ? "Active" : "Deactivated" }}</td>
        <td>
            <button type="button" class="btn btn-warning" style="margin-right: 10px;" @click.prevent="">
                <i class="bi bi-pencil-square"></i>
            </button>
            <button type="button" class="btn btn-danger" @click.prevent="">
                <i class="bi bi-trash"></i>
            </button>
        </td>
    </tr>
</template>
  
<script>

export default {
    name: "UserTableEntry",
    props: {
        item: Object,
    },
    components: {
    },
    methods: {
        //   async cancel() {
        //     try {
        //       const ok = await this.$refs.confirmDialogue.show({
        //         title: 'แก้ไขสถานะคำสั่งซื้อ',
        //         message: 'คุณต้องการจะยกเลิกสินค้าใช่ไหม?',
        //         okButton: 'ยืนยัน',
        //       });

        //       if (ok && !this.orderItem.cancel) {
        //         await cancelOrder(this.orderItem.id)
        //         this.$emit('clicked', "")
        //       } else {
        //         // nothing.
        //       }
        //     } catch (error) {
        //       console.log("error:", error);
        //     }
        //   }
    }
}
</script>
  
<style scoped></style>