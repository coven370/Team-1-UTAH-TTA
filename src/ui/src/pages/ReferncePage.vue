<template>
  <div>
    <div class="referenceContainer">
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
            <div :class="message.from + 'Message'" :id="message.id + 'message'">
              {{ message.message }}
            </div>
            <div class="eduKid messageHeader" v-if="message.from === 'ai'">EduKid</div>
          </div>
        </div>
        <div class="d-flex justify-content-center">
          <div class="referenceExplanation">
            <h4>Expert Reference</h4>
            <p>Ask me anything about teaching or student behavior. I will pull for a large knowledge set on education and will think about my response before giving you an answer.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked';
import AIAPIService from "@/servicehandlers/AIAPIService";

const aiService = new AIAPIService()
export default {
  name: "ReferencePage",
  data() {
    return {
      userInput: '',
      messages: [],
      reference: {},
      loading: false,
      optionsOpen: true,
      rawMessages: [],
    };
  },
  async mounted() {
    //console.clear();
    this.messages.reverse();
    this.rawMessages.push({role: 'system', content: 'You are an expert in elementary education.'})
  },
  methods: {
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
        messageObj.message += fullText.charAt(currentIndex);

        document.getElementById(messageObj.id + 'message').innerHTML = marked(messageObj.message);

        currentIndex++;

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
    }

  },
};
</script>

<style scoped>
.referenceExplanation{
  background-color: var(--white-green);
  padding: 15px;
  border-radius: 15px;
  text-align: center;
  width: 75%;
}
.referenceContainer {
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
