<template>
  <div class="overlay" v-if="isVisible">
    <div class="popUpContainer">
      <div class="popUp">
<!--        <i class="el-icon-close closeButton" @click="close"></i>-->
        <i class="el-icon-arrow-left backButton" @click="mode = 'Login'" v-if="mode !== 'Login'" ></i>
        <div class="loginContainer" v-if="this.mode === 'Login'">
          <h1>{{mode}}</h1>
          <div class="inputs">
            <input v-model="login.email" placeholder="Email"/>
            <input type="password" v-model="login.password" placeholder="Password"/>
          </div>
          <div>
            <el-button type="info" @click="mode = 'Forgot Password'">Forgot Password</el-button>
            <el-button type="info" @click="mode = 'Sign Up'">Sign Up</el-button>
            <el-button type="success">Login</el-button>
          </div>
        </div>
        <div class="loginContainer" v-if="this.mode === 'Sign Up'">
          <h1>{{mode}}</h1>
          <div class="inputs">
            <input v-model="newUser.email" placeholder="Email"/>
            <input type="password" v-model="newUser.password" placeholder="Password"/>
            <input v-model="newUser.full_name" placeholder="Full Name"/>
          </div>
          <div>
            <el-button type="success" @click="createNewUser">Submit</el-button>
          </div>
        </div>
        <div class="loginContainer" v-if="this.mode === 'Forgot Password'">
          <h1>{{mode}}</h1>
          <div class="inputs">
            <input v-model="userEmail" placeholder="Recovery Email"/>
          </div>
          <div>
            <el-button type="success">Submit</el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UsersAPIService from "@/servicehandlers/UsersAPIService";

const userAPIService = new UsersAPIService()
export default {
  name: "LoginModal",
  props: {
    isVisible: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      mode: 'Login',
      login: {
        email: '',
        password: '',
      },
      newUser: {
        email: '',
        password: '',
        full_name: '',
      },
      userEmail: '',
    }
  },
  mounted() {
    console.clear()
    this.mode = 'Login'
  },
  methods: {
    close(){
      this.mode = 'Login'
      this.$emit('close')
    },
    createNewUser(){
      console.log(this.newUser)
      return userAPIService.createUser(this.newUser, this.$router)
          .then(response => {
            console.log(response)
          })
    },
  }
};
</script>

<style scoped>
.inputs{
  width: 60%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}
.loginContainer{
  display: flex;
  width: 100%;
  flex-direction: column;
  align-items: center;
  margin: auto;
  gap: 75px;
}
input {
  width: 100%;
}
.overlay{
  z-index: 15;
  width: calc(100% - 16.6666% + 24px);
  margin-left: calc(16.6666% - 12px);
}
h1{
  padding: 0;
  margin: 0;
}
</style>
