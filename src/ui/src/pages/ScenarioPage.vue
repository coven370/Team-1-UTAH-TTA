<template>
  <div>
    <div class="scenarioContainer">
      <div class="inputContainer">
        <input type="text" v-model="userInput" @keyup.enter="sendMessage">
        <img class="sendImage" src="/img/send.svg" alt="" @click="sendMessage">
      </div>
      <div class="messagesContainer">
        <div class="messageWrapper" v-for="message of messages" :key="message.id">
          <div class="loading" v-if="message.loading">
            <i class="el-icon-loading loadingIcon"></i>
          </div>
          <div v-else>
            <div class="user messageHeader" v-if="message.from === 'user'">You</div>
            <div :class="message.from + 'Message'">
              {{ message.message }}
            </div>
            <div class="eduKid messageHeader" v-if="message.from === 'ai'">EduKid</div>
          </div>
        </div>
        <div class="d-flex justify-content-center">
          <div class="scenarioExplanation">
            <h4>{{scenario.name}}</h4>
            <p>{{scenario.description}}</p>
          </div>
        </div>
      </div>
    </div>
    <ScenarioOptions
        :is-visible="optionsOpen"
        @close="optionsOpen = false"
    ></ScenarioOptions>
  </div>
</template>

<script>
import ScenarioOptions from "@/components/ScenarioOptions.vue";
//import AIAPIService from "@/servicehandlers/AIAPIService";

//const aiService = new AIAPIService()
export default {
  name: "ScenarioPage",
  components: {
    ScenarioOptions
  },
  data() {
    return {
      userInput: '',
      messages: [],
      scenario: {},
      loading: false,
      optionsOpen: true,
    };
  },
  watch: {
    "$store.getters.scenario": function() {
      this.$nextTick(() => {
        this.scenario = this.$store.getters.scenario
        console.log(this.scenario)
        if (Object.keys(this.scenario).length > 0){
          this.optionsOpen = false
        } else {
          this.optionsOpen = true
          this.getScenario()
        }
      })
    }
  },
  mounted() {
    //console.clear();
    this.getScenario();

    // Prepopulate messages (for demo purposes)
    this.messages = [
      {
        id: 1,
        from: 'ai',
        message: 'Can I chew my gum during class?',
      },
      /*{
        id: 2,
        from: 'user',
        message: 'No, that will distract the other students.',
      },
      {
        id: 3,
        from: 'ai',
        message: 'I promise I won\'t chew very loud!',
      },*/
      // ... more messages
    ];
    this.messages.reverse();
  },
  methods: {
    getScenario() {
      this.scenario = {
        description: 'A student wants to chew gum during class',
        name: 'Gum in Class',
      };
    },
    sendMessage() {
      const userMsg = {
        id: this.messages.length + 1,
        from: 'user',
        message: this.userInput,
      };
      this.messages.unshift(userMsg);
      this.userInput = '';

      

      let fullText = 'I promise I won\'t chew very loud!';

      const aiResponse = {
        id: this.messages.length + 1,
        from: 'ai',
        message: '',
      };

      this.messages.unshift({loading: true})

      this.messages.unshift(aiResponse);

      this.typeWriterEffect(aiResponse, fullText, 3000);
    },
    typeWriterEffect(messageObj, fullText, duration = 3000) {
      let currentIndex = 0;
      const totalLetters = fullText.length;
      const interval = duration / totalLetters;

      const timer = setInterval(() => {
        // Append one letter at a time to the message property
        messageObj.message += fullText.charAt(currentIndex);
        currentIndex++;

        // When all letters have been added, clear the timer and turn off the loading indicator
        if (currentIndex >= totalLetters) {
          clearInterval(timer);
          for (let message of this.messages){
            if (message.loading){
              let index = this.messages.indexOf(message)
              this.messages.splice(index, 1)
            }
          }
        }
      }, interval);
    },
  },
};
</script>

<style scoped>
.scenarioExplanation{
  background-color: var(--white-green);
  padding: 15px;
  border-radius: 15px;
  text-align: center;
  width: 75%;
}
.scenarioContainer {
  width: 80%;
  height: 100vh;
  margin: auto;
  display: flex;
  flex-direction: column-reverse;
}
.inputContainer {
  display: flex;
  flex-direction: row;
  gap: 15px;
  justify-content: center;
  padding: 45px 0;
}
input {
  font-size: 20px;
  width: 80%;
}
.sendImage {
  width: 35px;
  cursor: pointer;
}
.sendImage:hover {
  transform: scale(120%);
}
.messagesContainer {
  display: flex;
  flex-direction: column-reverse;
  gap: 40px;
  overflow-x: auto;
  padding: 20px;
}
.messageWrapper {
  position: relative;
}
.aiMessage, .userMessage {
  width: 75%;
  border-radius: 15px;
  padding: 25px;
  font-size: 16px;
}
.aiMessage {
  background-color: var(--mint);
  margin-right: 25%;
}
.userMessage {
  background-color: var(--light-green);
  margin-left: 25%;
}
.messageHeader {
  font-size: 28px;
  position: absolute;
  top: -40px;
}
.eduKid {
  left: 20px;
}
.user {
  color: var(--blue);
  font-family: "Lilita One", serif;
  right: 20px;
}
</style>
