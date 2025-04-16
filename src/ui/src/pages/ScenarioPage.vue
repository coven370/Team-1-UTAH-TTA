<template>
  <div>
    <div class="scenarioContainer">
      <div class="inputContainer">
        <input type="text" v-model="userInput" @keyup.enter="sendMessage" :disabled="messages.some(data => data.loading)">
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
        <div class="d-flex justify-content-center" v-if="Object.keys(scenario).length > 0">
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
import AIAPIService from "@/servicehandlers/AIAPIService";

const aiService = new AIAPIService()
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
      rawMessages: [],
    };
  },
  watch: {
    "$store.getters.scenario": function() {
      this.$nextTick(() => {
        this.scenario = this.$store.getters.scenario
        this.optionsOpen = Object.keys(this.scenario).length <= 0;
        if (!this.optionsOpen){
          this.messages = []
          this.rawMessages = []
          this.getScenario()
        }
      })
    }
  },
  async mounted() {
    //console.clear();
    this.messages.reverse();

    console.log(await aiService.getScenario(this.$router))
  },
  methods: {
    async getScenario() {
      console.log(this.scenario)
      this.rawMessages.push({role: 'system', content: this.scenario.description})
      this.rawMessages.push({ role: 'user', content: 'Act like this student in a couple of sentences.'})

      this.messages.unshift({loading: true})

      let response = await aiService.sendMessage(this.rawMessages, this.$router)

      console.log(response)

      let fullText = response.message.content;
      this.rawMessages.push(response.message)

      const aiResponse = {
        id: this.messages.length + 1,
        from: 'ai',
        message: '',
      };

      this.messages.unshift(aiResponse);

      this.typeWriterEffect(aiResponse, fullText, 3000);
    },
    async sendMessage() {
      const userMsg = {
        id: this.messages.length + 1,
        from: 'user',
        message: this.userInput,
      };
      this.rawMessages.push({role: 'user', content: this.userInput})
      this.messages.unshift(userMsg);

      this.userInput = '';

      this.messages.unshift({loading: true})

      let response = await aiService.sendMessage(this.rawMessages, this.$router)

      console.log(response)

      let fullText = response.message.content;
      this.rawMessages.push(response.message)

      const aiResponse = {
        id: this.messages.length + 1,
        from: 'ai',
        message: '',
      };

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
