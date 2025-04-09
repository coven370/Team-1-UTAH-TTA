<template>
  <div>
    <h1>Home Page</h1>
    <LoginModal
        :is-visible="loginOpen"
        @close="loginOpen= false"
    />
  </div>
</template>

<script>
import LoginModal from "@/pages/LoginModal.vue";

export default {
  name: "HomePage",
  components: {LoginModal},
  data() {
    return {
      loginOpen: true
    }
  }
};
</script>

<style scoped>

</style>
