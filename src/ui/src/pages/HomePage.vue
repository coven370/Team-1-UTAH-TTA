<template>
<!--  <div v-if="$store.getters.loggedIn">-->
  <div>
    <div class="header">
      <h1><b>Overview</b></h1>
      <h4>User</h4>
    </div>
    <div class="line">
      <div class="card" style="width: 50%">
        <h4>You have completed 3 scenarios this week!!</h4>
        <h6>Top focus area: Positive Reinforcement</h6>
        <h6>Suggested Focus: <b>De-escalation</b></h6>
      </div>
      <div class="card" style="width: 50%">
        <h4>Quick Tips</h4>
        <h6>Give clear, simple instructions with visual cues.</h6>
      </div>
    </div>
    <div class="line">
      <div class="card" style="width: 100%">
        <h4>Recent Scenarios</h4>
        <div class="scenario">
          <h5>Tantrum during Math Time</h5>
          <p>A student throws a tantrum during math time, yelling and refusing to do the assignment after appearing frustrated.</p>
          <p>You stayed calm, which helped the class feel safe. Try offering choices or a quick break to help the student regain control.</p>
          <button>View Scenario</button>
        </div>
        <div class="scenario">
          <h5>New student refused to talk</h5>
          <p>A new student refuses to speak during class activities and avoids interaction with peers and the teacher.</p>
          <p>You gave the student space, which showed sensitivity. Try building trust through low-pressure activities or one-on-one check-ins to encourage communication.</p>
          <button>View Scenario</button>
        </div>
      </div>
    </div>
    <LoginModal
        :is-visible="loginOpen"
        @close="loginOpen = false"
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
.scenario{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 30px;
}
p{
  width: 33%;
}
.header{
  display: flex;
  padding: 30px 45px;
  justify-content: space-between;
  align-items: center;
}
.line{
  display: flex;
  padding: 30px;
  gap: 30px;
}
.card{
  background-color: var(--seasalt);
  padding: 30px;
  border-radius: 20px;
}
</style>
