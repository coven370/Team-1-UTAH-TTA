<template>
  <div class="overlay" v-if="isVisible">
    <div class="popUpContainer">
      <div class="popUp">
        <i class="el-icon-close closeButton" @click="close"></i>
        <h1>Scenario Options</h1>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ImprovePage",
  props: {
    isVisible: {
      type: Boolean,
      required: true
    }
  },
  methods: {
    close(){
      this.$emit('close')
    },
  }
};
</script>

<style scoped>
.overlay{
  z-index: 15;
  width: calc(100% - 16.6666% + 24px);
  margin-left: calc(16.6666% - 12px);
}
</style>
