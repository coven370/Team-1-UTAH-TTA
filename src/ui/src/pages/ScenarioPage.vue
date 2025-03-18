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
            <div class="user messageHeader" v-if="message.from === 'user'">User</div>
            <div :class="message.from + 'Message'">
              {{ message.id }} {{ message.message }}
            </div>
            <div class="eduKid messageHeader" v-if="message.from === 'ai'">EduKid</div>
          </div>
        </div>
        <div class="scenarioExplanation"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ScenarioPage",
  data() {
    return {
      userInput: '',
      messages: [],
      scenario: {},
      loading: false,
    };
  },
  mounted() {
    console.clear();
    this.getScenario();

    // Prepopulate messages (for demo purposes)
    this.messages = [
      {
        id: 1,
        from: 'ai',
        message: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...',
      },
      {
        id: 2,
        from: 'user',
        message: 'User message example...',
      },
      // ... more messages
    ];
    this.messages.reverse();
  },
  methods: {
    getScenario() {
      this.scenario = {
        description: 'Description',
        name: 'Name',
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

      let fullText = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.';

      fullText += fullText

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
