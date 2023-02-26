<template>
    <div class="pagination-component">
        <div class="information-section" style="text-align: center;">
            <span> {{ totalItems ? currentPage + 1 : 0 }} from {{ totalPages }} pages, found {{ totalItems }} users </span>
        </div>
        <div class="information-section row">
            <div class="col">
                <button type="button" class="btn btn-secondary" :disabled="!hasPrevious" @click.prevent="changePage(-1)">&#x3c;- Previous</button>
            </div>
            <div class="col" style="text-align: right;">
                <button type="button" class="btn btn-secondary" :disabled="!hasNext" @click.prevent="changePage(1)">Next -&#x3e;</button>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: "PaginationInformationComponent",
    props: {
        currentPage: Number,
        totalPages: Number,
        totalItems: Number,
        hasPrevious: Boolean,
        hasNext: Boolean
    },
    components: {
    },
    data() {
        return {
            page: 1
        };
    },
    mounted() {
        this.page = this.$props.currentPage + 1
    },
    computed: {
    },
    methods: {
        changePage(navigator) {
            const newCurrentPage = this.currentPage + navigator;
            this.$emit('clickedChangeCurrentPage', newCurrentPage);
        },
        changePageFromInputField() {
            this.$emit('clickedChangeCurrentPage', this.page - 1);
        }
    },
    watch: {
        currentPage(value) {
            /* 
                Once the prop mounted during creation,
                the $props.currentPage is never updated.
                So, need this watch() method to update the value 
                or else the dropdown select would not change.
            */
            this.page = value + 1;
        },
    }
}
</script>

<style scoped>
    .page-number {
        width: 100px;
    }
    .information-section {
        margin-bottom: 10px;
    }
    select{
        float: right;
    }
</style>