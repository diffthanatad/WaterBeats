<template>
  <div id="nav" v-if="hide">
    <NavigationBar />
  </div>
  <router-view/>
</template>

<script>
import NavigationBar from '@/components/NavigationBar.vue';

export default {
  name: 'AppView',
  components: {
    NavigationBar
  },
  computed: {
    hide () {
      return this.$route.path !== "/login"
    },
    loading() {
      return this.$store.getters['loading/isLoading'];
    }
  },
}
</script>

<style>
/* * {
  font-family: 'Kumbh Sans', sans-serif;
} */
</style>
