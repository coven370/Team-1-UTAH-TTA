<template>
  <div>
    <div class="cardContainer">
      <div class="card" id="card">
        <h3>"{{phrases[0].phrase}}"</h3>
        <div class="footer">
          <button class="successButton" @click="processCard('keep')">Sounds like a 2nd Grader</button>
          <button @click="processCard('shuffle')">I'm not really sure</button>
          <button class="dangerButton" @click="processCard('throw')">That's not a 2nd Grader</button>
        </div>
      </div>
      <div id="behind" class="behindContainer">
        <div class="behindWrapper">
          <div class="card behind"
               v-for="phrase of phrases.slice(1, phrases.length - 1)" v-bind:key="phrase.id"
               :style="behindStyles(phrases.indexOf(phrase))"
          >
            <h3 v-if="phrases.indexOf(phrase) === 1">"{{phrases[1].phrase}}"</h3>
            <div v-if="phrases.indexOf(phrase) === 1" class="footer">
              <button class="successButton">Sounds like a 2nd Grader</button>
              <button>I'm not really sure</button>
              <button class="dangerButton">That's not a 2nd Grader</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <improve-accept-pop-up
        :is-visible="openAcceptPopUp"
        @close="toggleAcceptPopUp"
    ></improve-accept-pop-up>
    <div class="top" id="top"></div>
    <div class="bottom"></div>
    <div class="trash" id="trash">
      <div class="lines">
        <div class="leftLine"></div>
        <div class="midLine"></div>
        <div class="rightLine"></div>
      </div>
    </div>
  </div>
</template>

<script>
import ImproveAcceptPopUp from "@/components/ImproveAcceptPopUp.vue";
export default {
  name: "ImprovePage",
  components: {
    ImproveAcceptPopUp,
  },
  data (){
    return {
      openAcceptPopUp: true,
      phrases: [],
      behindValues: {
        zIndex: 1,
        scale: 2,
        transform: 7,
        opacity: .1,
      }
    }
  },
  mounted() {
    console.clear()
    this.openAcceptPopUp = !this.$store.getters.improveAccepted
    this.loadTestData()
  },
  methods: {
    loadTestData(){
      this.phrases = [
        {
          id: 1,
          phrase: "Can I read my book right now?",
        },
        {
          id: 2,
          phrase: "Can I read my book right now?",
        },
        {
          id: 3,
          phrase: "Can I read my book right now?",
        },
        {
          id: 4,
          phrase: "Can I read my book right now?",
        },
        {
          id: 5,
          phrase: "Can I read my book right now?",
        },
        {
          id: 6,
          phrase: "Can I read my book right now?",
        },
        {
          id: 7,
          phrase: "Can I read my book right now?",
        },
        {
          id: 8,
          phrase: "Can I read my book right now?",
        },
        {
          id: 9,
          phrase: "Can I read my book right now?",
        },
        {
          id: 10,
          phrase: "Can I read my book right now?",
        },
      ]
    },
    getNewPhrase(){
      this.phrases.splice(0, 1)
      let newId = this.phrases[this.phrases.length - 1].id +1
      let temp = {
        id: newId,
        phrase: "Can I read my book right now?",
      }
      this.phrases.push(temp)
    },
    toggleAcceptPopUp(){
      this.openAcceptPopUp = !this.openAcceptPopUp
    },
    processCard(type){
      let card = document.getElementById('card')
      let behind = document.getElementById("behind");
      let folderTop = document.getElementById('top')
      let trash = document.getElementById('trash')
      switch (type){
        case 'throw':
          card.classList.add('throw')
          trash.classList.add('vibrate')
          break
        case 'shuffle':
          card.classList.add('shuffle')
          break
        case 'keep':
          card.classList.add('keep')
          folderTop.classList.add('openFolder')
          break
      }
      behind.classList.add('bringForward')

      setTimeout(() => {
        card.classList.remove('throw')
        card.classList.remove('shuffle')
        card.classList.remove('keep')
        behind.classList.remove('bringForward')
        folderTop.classList.remove('openFolder')
        trash.classList.remove('vibrate')

        this.getNewPhrase()
      }, 1000)
    },
    behindStyles(index){
      let transform = 50 + (index * this.behindValues.transform)
      let scale = 100 - (index * this.behindValues.scale)
      let zIndex = 10 - (index * this.behindValues.zIndex)
      let redDist = (244 - 167) / this.phrases.length
      let greenDist = (247 - 162) / this.phrases.length
      let blueDist = (245 - 169) / this.phrases.length
      let red = 244 - ((index - 1) * redDist)
      let green = 247 - ((index - 1) * greenDist)
      let blue = 245 - ((index - 1) * blueDist)
      return `transform: translate(0, -${transform}%) scale(${scale}%); z-index: ${zIndex}; background-color: rgb(${red}, ${green}, ${blue})`
    }
  }
};
</script>

<style scoped>
.trash{
  position: absolute;
  bottom: -10%;
  right: -15%;
  width: 600px;
  height: 700px;
  background-color: #7a7a7a;
  clip-path: polygon(0 0, 100% 0, 88% 100%, 12% 100%);
  transform: rotate(-60deg);
  z-index: 11;
  border-radius: 50px;
}
.lines{
  position: relative;
  width: 100%;
  height: 100%;
}
.leftLine, .midLine, .rightLine{
  background-color: var(--quartz);
  width: 12%;
  height: 78%;
  position: absolute;
  top: 50%;
  left: 50%;
  border-radius: 300px;
}
.leftLine{
  webkit-transfrom: translate(-250%, -48%) rotate(-4deg);
  transform: translate(-250%, -48%) rotate(-4deg);
}
.midLine{
  webkit-transfrom: translate(-50%, -50%);
  transform: translate(-50%, -50%);
}
.rightLine{
  webkit-transfrom: translate(150%, -48%) rotate(4deg);
  transform: translate(150%, -48%) rotate(4deg);
}
.vibrate {
  animation: vibrate 1s linear infinite;
}

@keyframes vibrate {
  0% {
    transform: translate(0) rotate(-60deg);
  }
  30% {
    transform: translate(0) rotate(-60deg);
  }
  35% {
    transform: translate(-2px, 2px) rotate(-60deg);
  }
  40% {
    transform: translate(-2px, -2px) rotate(-60deg);
  }
  45% {
    transform: translate(2px, 2px) rotate(-60deg);
  }
  50% {
    transform: translate(2px, -2px) rotate(-60deg);
  }
  55% {
    transform: translate(4px, 4px) rotate(-60deg);
  }
  60% {
    transform: translate(4px, -4px) rotate(-60deg);
  }
  65% {
    transform: translate(-2px, 2px) rotate(-60deg);
  }
  70% {
    transform: translate(-2px, -2px) rotate(-60deg);
  }
  80% {
    transform: translate(2px, 2px) rotate(-60deg);
  }
  90% {
    transform: translate(2px, -2px) rotate(-60deg);
  }
  100% {
    transform: translate(0) rotate(-60deg);
  }
}

.folderContainer{
  width: 750px;
  height: 1500px;
  position: absolute;
  top: -80%;
  left: 0;
  transform: rotate(50deg);
}
.folder{
  width: 100%;
  height: 100%;
  position: relative;
}
.top {
  width: calc(750px * .98);
  height: calc(1500px * .98);
  top: -80%;
  left: 0;
  transform: rotate(50deg);
  background-color: #f4e9cd;
  position: absolute;
  z-index: 12;
  box-shadow: #918a78 5px 10px 10px;
  border: none;
}
.bottom {
  width: calc(750px);
  height: calc(1500px);
  top: -80%;
  left: 0;
  transform: rotate(50deg);
  background-color: #ded3b8;
  position: absolute;
  z-index: 0;
  box-shadow: #7d7a80 10px 10px 10px;
  border: none;
}

.top::before {
  position: absolute;
  right: -100px;
  top: 65%;
  height: 600px;
  width: 500px;
  background: inherit;
  border-top-right-radius: 30px;
  border-bottom-right-radius: 30px;
  box-shadow: inherit;
  border: none;
  content: "To Keep";
  padding: 30px 15px;
  font-size: 60px;
  writing-mode: vertical-rl;
  font-family: "Handlee", serif;
  font-weight: 400;
  font-style: normal;
}

.bottom::before {
  content: "";
  position: absolute;
  right: -100px;
  top: 65%;
  height: 600px;
  width: 500px;
  background: inherit;
  border-top-right-radius: 30px;
  border-bottom-right-radius: 30px;
  box-shadow: inherit;
  border: none;
}

.openFolder{
  animation: openFolder 1s ease-in-out;
}

@keyframes openFolder {
  0% {
    transform: translate(0, 0) rotate(50deg);
    box-shadow: #918a78 5px 10px 10px;
  }
  50% {
    transform: translate(-10%, -10%) rotate(50deg);
    box-shadow: rgba(145, 138, 120, 0.25) 100px 50px 40px;
  }
  100% {
    transform: translate(0, 0) rotate(50deg);
    box-shadow: #918a78 5px 10px 10px;
  }
}

h3{
  text-align: center;
}
.cardContainer{
  position: relative;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.card {
  border: none;
  border-radius: 10px;
  background-color: var(--seasalt);
  width: 50%;
  height: 25%;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  z-index: 10;
}
.footer{
  width: 100%;
  display: flex;
  justify-content: space-evenly;
}
.behindContainer{
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 5;
  opacity: 90%;
}
.behindWrapper{
  position: relative;
  width: 100%;
  height: 100%;
}
.behind{
  position: absolute;
  top: 50%;
  left: 25%;
  webkit-transform: translate(0, -50%);
  transform: translate(0, -50%);
  width: 50%;
  height: 25%;
  z-index: 9;
}
.throw{
  animation: throw 1s ease-in-out;
}
@keyframes throw {
  0% {
    transform: translate(0, 0) rotate(0deg);
    background-color: var(--seasalt);
  }
  50%{
    transform: translate(150%, 150%) rotate(50deg);
    background-color: var(--light-red);
  }
  100%{
    transform: translate(300%, 300%) rotate(0deg);
    background-color: var(--seasalt);
  }
}
.keep{
  animation: keep 1s ease-in-out;
}
@keyframes keep {
  0% {
    transform: translate(0, 0) rotate(0deg);
    background-color: var(--seasalt);
  }
  50%{
    background-color: var(--light-green);
  }
  100%{
    transform: translate(-200%, -500%) rotate(-70deg);
    background-color: var(--seasalt);
  }
}
.shuffle{
  animation: shuffle 1s ease-in-out;
}
@keyframes shuffle {
  0% {
    transform: translate(0, 0) scale(1);
    z-index: 10;
    opacity: 1;
  }
  50%{
    transform: translate(-15%, 120%) rotate(10deg);
    z-index: 5;
    opacity: 1;
  }
  100% {
    transform: translate(0, 0) scale(.75);
    z-index: 0;
    opacity: .5;
  }
}
.bringForward{
  animation: bringForward 1s ease-in-out;
}
@keyframes bringForward {
  0% {
    transform: translate(0, 0) scale(100%);
    opacity: 90%;

  }
  100%{
    transform: translate(0, 2%) scale(102%);
    opacity: 100%;
  }
}

</style>
