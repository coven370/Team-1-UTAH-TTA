<template>
  <div class="overlay" v-if="isVisible">
    <div class="popUpContainer">
      <div class="popUp">
<!--        <i class="el-icon-close closeButton" @click="close"></i>-->
        <i class="el-icon-arrow-left backButton" @click="changeMode('Login')" v-if="mode !== 'Login'" ></i>
        <div class="loginContainer" v-if="this.mode === 'Login'">
          <h1>{{mode}}</h1>
          <div class="inputs">
            <div style="width: 100%">
              <input v-model="loginData.username" placeholder="Email"/>
              <div style="text-align: left">
                <span class="smallErrorText" style="color: transparent">.</span>
              </div>
            </div>
            <input type="password" v-model="loginData.password" placeholder="Password"/>
          </div>
          <div>
            <button @click="changeMode('Forgot Password')">Forgot Password</button>
            <button @click="changeMode('Sign Up')">Sign Up</button>
            <button @click="login" class="successButton">Login</button>
          </div>
        </div>
        <div class="loginContainer" v-if="this.mode === 'Sign Up'">
          <h1>{{mode}}</h1>
          <div class="inputs">
            <div style="width: 100%">
              <input v-model="newUser.email" placeholder="Email" @keyup="validateInput('email', newUser.email, '', $event)"/>
              <div style="text-align: left">
                <span v-if="errors.email === -1" class="smallErrorText">Please enter a valid Email</span>
                <i v-else-if="errors.email === 1" class="el-icon-check greenText"></i>
                <span class="smallErrorText" style="color: transparent">.</span>
              </div>
            </div>
            <div style="width: 100%">
              <input type="password" v-model="newUser.password" placeholder="Password" @keyup="validateInput('password', newUser.password, '', $event)"/>
              <div style="text-align: left">
                <span v-if="errors.password === -1" class="smallErrorText">Password must be at least 8 characters</span>
                <i v-else-if="errors.password === 1" class="el-icon-check greenText"></i>
                <span class="smallErrorText" style="color: transparent">.</span>
              </div>
            </div>
            <div style="width: 100%">
              <input type="password" v-model="newUser.confirm" placeholder="Confirm Password" @keyup="validateInput('confirm', newUser.password, newUser.confirm, $event)"/>
              <div style="text-align: left">
                <span v-if="errors.confirm === -1" class="smallErrorText">Passwords don't match</span>
                <i v-else-if="errors.confirm === 1" class="el-icon-check greenText"></i>
                <span class="smallErrorText" style="color: transparent">.</span>
              </div>
            </div>
            <div style="width: 100%">
              <input v-model="newUser.full_name" placeholder="Full Name" @keyup="validateInput('name', newUser.full_name, '', $event)"/>
              <div style="text-align: left">
                <span v-if="errors.full_name === -1" class="smallErrorText">Please enter a valid Email</span>
                <i v-else-if="errors.full_name === 1" class="el-icon-check greenText"></i>
                <span class="smallErrorText" style="color: transparent">.</span>
              </div>
            </div>
          </div>
          <div>
            <button class="successButton" @click="createNewUser" :disabled="isFormInvalid">Submit</button>
          </div>
        </div>
        <div class="loginContainer" v-if="this.mode === 'Forgot Password'">
          <h1>{{mode}}</h1>
          <div class="inputs">
            <div style="width: 100%">
              <input v-model="userEmail" placeholder="Recovery Email" @keyup="validateInput('email', userEmail, '', $event)"/>
              <div style="text-align: left">
                <span v-if="errors.email === -1" class="smallErrorText">Please enter a valid Email</span>
                <i v-else-if="errors.email === 1" class="el-icon-check greenText"></i>
                <span class="smallErrorText" style="color: transparent">.</span>
              </div>
            </div>
          </div>
          <div>
            <button class="successButton" :disabled="isFormInvalid" @click="recoverPassword">Submit</button>
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
      errors: {
        email: 0,
        password: 0,
        confirm: 0,
        full_name: 0,
      },
      loginData: {
        grant_type: 'password',
        username: '',
        password: '',
      },
      newUser: {
        email: '',
        password: '',
        full_name: '',
        confirm: '',
      },
      userEmail: '',
      isFormInvalid: true,
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
    changeMode(mode){
      this.mode = mode
      this.validateInput(null)
      if (mode === 'Login'){
        this.login= {
          email: '',
          password: '',
        }
        this.newUser = {
          email: '',
          password: '',
          full_name: '',
          confirm: '',
        }
        this.userEmail = ''
      }
    },
    validateInput(type, value, confirm, event) {
      if (event && event.key === 'Tab') return;

      switch (type) {
        case 'email': {
          let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailRegex.test(value)) {
            this.errors.email = -1;
          } else {
            this.errors.email = 1;
          }
          break;
        }
        case 'password':
          if (value.length < 8) {
            this.errors.password = -1;
          } else {
            this.errors.password = 1;
          }
          break;
        case 'confirm':
          if (value !== confirm) {
            this.errors.confirm = -1;
          } else {
            this.errors.confirm = 1;
          }
          break;
        case 'name':
          if (!value) {
            this.errors.full_name = -1;
          } else {
            this.errors.full_name = 1;
          }
          break;
        default:
          if (this.mode === 'Forgot Password'){
            this.errors = {
              email: 0,
              password: 1,
              confirm: 1,
              full_name: 1,
            }
          } else {
            this.errors = {
              email: 0,
              password: 0,
              confirm: 0,
              full_name: 0,
            };
          }
      }
      this.isFormInvalid = Object.values(this.errors).some(value => value <= 0)
    },
    createNewUser(){
      console.log(this.newUser)
      return userAPIService.createUser(this.newUser, this.$router)
          .then(response => {
            console.log(response)
            this.changeMode('Login')
          })
    },
    recoverPassword(){
      return userAPIService.resetPassword(this.userEmail, this.$router)
          .then(response => {
            console.log(response)
            this.changeMode('Login')
          })
    },
    // When calling the login function:
    login() {
      console.log(this.loginData);
      // Use spread operator to create a plain object copy of loginData
      return userAPIService.CommonAPIService.login({ ...this.loginData }, this.$router, this.$store, [])
          .then(response => {
            if (response && response.success) {
              this.close();
            }
          });
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
  gap: 10px;
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
