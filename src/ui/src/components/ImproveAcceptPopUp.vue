<template>
  <div class="overlay" v-if="isVisible">
    <div class="popUpContainer">
      <div class="popUp">
<!--        <i class="el-icon-close closeButton" @click="close"></i>-->
        <h1>Improve <span class="eduKid">EduKid</span></h1>
        <h6>
          Thank you for your interest in helping us improve <span class="eduKid">EduKid</span>!
        </h6>
        <p>
          Here you will see a phase or an action. Your job is to decide whether the phase/action is something that a 2nd grade would do or say. Using the buttons under each of the prompts, you can help the ai become a better and more child like 2nd grader.
        </p>
        <div class="popUpFooter">
          <el-button type="success" @click="accept">Let Me Help Improve EduKid</el-button>
        </div>
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
    accept(){
      this.$store.dispatch('ACCEPT_IMPROVE')
      this.close()
    }
  }
};
</script>

<style scoped>
</style>
