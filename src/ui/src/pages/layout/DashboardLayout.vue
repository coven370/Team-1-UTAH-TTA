<template>
  <div class="fullContainer">
    <div class="row fullHeight">
      <div class="col-sm-2 sidebar">
        <h1 @click="goToPage('Home', {})" class="siteLogo">EduKid</h1>
        <div v-for="tab of tabs" v-bind:key="tab.name">
          <div class="sidebarItem" :class="[$route.name === tab.name ? 'selected' : null]" @click="goToPage(tab.name, {})">
            <i :class="tab.icon" class="tabIcon"></i>
            <h4 class="itemLabel">{{tab.label}}</h4>
          </div>
          <div class="children" v-for="(child, i) of tab.children" v-bind:key="i" @click="goToScenario(child)" :class="[child === selectedScenario ? 'selected' : null]">
            <h5 class="childLabel text-center">{{child.label}}</h5>
          </div>
        </div>
        <div class="mintCircle"></div>
        <div class="greenCircle"></div>
        <div class="footer">
          <div class="logoutText" @click="logout">Log Out</div>
        </div>
      </div>
      <div class="col-sm-10 content" :class="$route.name === 'ImproveAI' ? 'circleBack' : 'cubeBack'">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DashboardLayout",
  data(){
    return {
      tabs: [
        {
          label: 'Home',
          name: 'Home',
          icon: 'el-icon-menu',
        },
        {
          label: 'Scenario',
          name: 'Scenario',
          icon: 'el-icon-data-line',
          children: [
            {
              label: 'Scenario 1',
            },
            {
              label: 'Scenario 2',
            },
            {
              label: 'Scenario 3',
            },
            {
              label: 'Scenario 4',
            },
            {
              label: 'Scenario 5',
            },
          ],
        },
        {
          label: 'Improve',
          name: 'ImproveAI',
          icon: 'el-icon-notebook-1',
        },
      ],
      selectedScenario: null,
    }
  },
  methods: {
    goToPage(name, params){
      if (this.$route.name !== name){
        this.$router.push({
          name: name,
          params: params,
        })
      }
      this.selectedScenario = {}
    },
    async goToScenario(scene){
      await this.goToPage('Scenario', {scenario: scene})
      this.selectedScenario = scene
    },
    logout(){
      this.$store.dispatch('LOGOUT')
      this.goToPage('Home', {})
    },
  }
};
</script>

<style scoped>
.fullContainer{
  width: 100vw;
  height: 100vh;
}
.fullHeight{
  height: 100%;
}
.sidebar{
  background-color: var(--dark-blue);
  padding: 20px 40px;
  color: var(--seasalt);
  clip-path: polygon(0 0, 100% 0, 100% 100%, 0% 100%);
  z-index: 20;
  position: relative;
}
.sidebarItem{
  display: flex;
  align-items: center;
  padding: 15px 20px;
  font-size: 24px;
  cursor: pointer;
}
.selected{
  background-color: var(--blue);
  border-radius: 10px;
}
.tabIcon{
  font-size: 24px;
  margin-right: 15px;
}
.itemLabel{
  margin: 0;
}
.childLabel{
  margin: 7px 0;
  padding: 7px 0;
  cursor: pointer;
}
.siteLogo{
  font-family: "Lilita One", serif;
  font-size: 60px;
  color: var(--orange);
  cursor: pointer;
}
.mintCircle{
  background-color: var(--mint);
  width: 400px;
  aspect-ratio: 1 / 1;
  border-radius: 50%;
  position: absolute;
  bottom: -50px;
  left: -150px;
}
.greenCircle{
  background-color: var(--light-green);
  width: 400px;
  aspect-ratio: 1 / 1;
  border-radius: 50%;
  position: absolute;
  bottom: -200px;
  left: 25px;
}
.footer{
  color: var(--blue);
  width: 100%;
  position: absolute;
  bottom: 0;
  left: 0;
  align-self: flex-end;
  margin-bottom: 30px;
  display: flex;
  justify-content: space-around;
}
.logoutText{
  cursor: pointer;
}
.circleBack{
  background: radial-gradient(circle, var(--quartz) 50%, rgba(167, 162, 169, 0.75) 60%, rgba(0,0,0,0) 100%);
}
.cubeBack{
  background: linear-gradient(90deg, rgba(0,0,0,0) 0%, rgba(167, 162, 169, 0.75) 15%, var(--quartz) 40%, var(--quartz) 60%, rgba(167, 162, 169, 0.75) 85%, rgba(0,0,0,0) 100%);
}
</style>