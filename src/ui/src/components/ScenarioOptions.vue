<template>
  <div class="overlay" v-if="isVisible">
    <div class="popUpContainer">
      <div class="popUp">
<!--        <i class="el-icon-close closeButton" @click="close"></i>-->
        <h1>Scenario Options</h1>
        <div class="scrollable">
          <div class="section" v-for="(section, i) of sections" v-bind:key="i">
            <h3>{{section.label}}</h3>
            <div class="line" v-for="(key, i) of Object.keys(section.object)" v-bind:key="i">
              <label>{{section.object[key].label}}:</label>
              <input v-if="section.object[key].type === 'text'" type="text" v-model="section.object[key].value">
              <select v-else-if="section.object[key].type === 'select'" v-model="section.object[key].value">
                <option v-for="option of section.object[key].list" v-bind:key="option.value" :value="option.value">{{option.label}}</option>
              </select>
            </div>
            <div class="footer">
              <button class="dangerButton smallButton" @click="clearSection(section)">Clear</button>
              <button class="primaryButton smallButton" @click="randomizeSection(section, false)">Randomize Blank</button>
              <button class="primaryButton smallButton" @click="randomizeSection(section, true)">Randomize All</button>
            </div>
          </div>
        </div>
        <br>
        <button class="successButton" @click="startScenario">Start Scenario</button>
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
  data(){
    return {
      sections: [
        {
          label: 'Student Profile',
          object: {
            name: {
              label: 'Student Name',
              type: 'text',
              list: [
                { label: "Alex", value: "Alex" },
                { label: "Jamie", value: "Jamie" },
                { label: "Taylor", value: "Taylor" },
                { label: "Jordan", value: "Jordan" },
                { label: "Casey", value: "Casey" },
              ],
              value: '',
            },
            gradeLevel: {
              label: 'Grade Level',
              type: 'select',
              list: [
                { label: "1st Grade", value: 1 },
                { label: "2nd Grade", value: 2 },
                { label: "3rd Grade", value: 3 },
              ],
              value: '',
            },
            personalityTrait: {
              label: 'Personality Trait',
              type: 'select',
              list: [
                { label: "Shy", value: "shy" },
                { label: "Talkative", value: "talkative" },
                { label: "Easily Distracted", value: "distracted" },
                { label: "Energetic", value: "energetic" },
                { label: "Defiant", value: "defiant" },
                { label: "Curious", value: "curious" },
              ],
              value: '',
            },
            emotionalState: {
              label: 'Emotional State',
              type: 'select',
              list: [
                { label: "Happy", value: "happy" },
                { label: "Frustrated", value: "frustrated" },
                { label: "Anxious", value: "anxious" },
                { label: "Tired", value: "tired" },
                { label: "Overwhelmed", value: "overwhelmed" },
                { label: "Angry", value: "angry" },
              ],
              value: '',
            },
            backgroundContext: {
              label: 'Background Context',
              type: 'select',
              list: [
                { label: "New student", value: "new" },
                { label: "Has sibling in school", value: "sibling" },
                { label: "Learning disability", value: "disability" },
                { label: "English as second language", value: "esl" },
                { label: "Recently moved", value: "moved" },
              ],
              value: '',
            },
          },
        },
        {
          label: 'Academic Context',
          object: {
            activity: {
              label: 'Subject/Activity',
              type: 'select',
              list: [
                { label: "Reading Circle", value: "reading" },
                { label: "Math Lesson", value: "math" },
                { label: "Free Time", value: "free" },
                { label: "Group Project", value: "group" },
                { label: "Recess Transition", value: "recess" },
              ],
              value: '',
            },
            difficultyLevel: {
              label: 'Activity Difficulty Level',
              type: 'select',
              list: [
                { label: "Easy", value: "easy" },
                { label: "Appropriate", value: "appropriate" },
                { label: "Challenging", value: "challenging" },
                { label: "Overwhelming", value: "overwhelming" },
              ],
              value: '',
            },
          },
        },
        {
          label: 'Environment Factors',
          object: {
            classroomSettings: {
              label: 'Classroom Setting',
              type: 'select',
              list: [
                { label: "Calm and Quiet", value: "calm" },
                { label: "Noisy", value: "noisy" },
                { label: "Chaotic", value: "chaotic" },
                { label: "Testing Environment", value: "testing" },
                { label: "Substitute Teacher", value: "substitute" },
              ],
              value: '',
            },
            timeOfDay: {
              label: 'Time of Day',
              type: 'select',
              list: [
                { label: "Morning", value: "morning" },
                { label: "After Lunch", value: "afternoon" },
                { label: "End of Day", value: "end" },
              ],
              value: '',
            },
            recentClassEvent: {
              label: 'Recent Class Event',
              type: 'select',
              list: [
                { label: "Returned from recess", value: "recess" },
                { label: "Fire drill just ended", value: "fireDrill" },
                { label: "Class just got scolded", value: "scolding" },
                { label: "Birthday celebration", value: "birthday" },
              ],
              value: '',
            },
          },
        },
        {
          label: 'Behavior Challenge',
          object: {
            typeOfBehavior: {
              label: 'Type of Behavior',
              type: 'select',
              list: [
                { label: "Refusing to follow directions", value: "refusal" },
                { label: "Talking out of turn", value: "interrupting" },
                { label: "Arguing with peers", value: "arguing" },
                { label: "Tantrum", value: "tantrum" },
                { label: "Silent and disengaged", value: "silent" },
                { label: "Overly excited", value: "excited" },
              ],
              value: '',
            },
            frequency: {
              label: 'Frequency',
              type: 'select',
              list: [
                { label: "One-time", value: "once" },
                { label: "Recurring", value: "recurring" },
              ],
              value: '',
            },
          },
        },
        {
          label: 'Learning Objective',
          object: {
            typeOfBehavior: {
              label: 'Objective',
              type: 'select',
              list: [
                { label: "De-escalation", value: "deescalation" },
                { label: "Positive reinforcement", value: "reinforcement" },
                { label: "Giving clear directions", value: "directions" },
                { label: "Offering choices", value: "choices" },
                { label: "Empathic listening", value: "listening" },
                { label: "Redirecting behavior", value: "redirecting" },
                { label: "Setting boundaries", value: "boundaries" },
              ],
              value: '',
            },
          },
        },
      ],
    }
  },
  methods: {
    close(){
      this.$emit('close')
    },
    clearSection(section){
      for (let key of Object.keys(section.object)){
        section.object[key].value = ''
      }
    },
    randomizeSection(section, all){
      for (let key of Object.keys(section.object)){
        if (all || !section.object[key].value){
          section.object[key].value = getRandomElementValue(section.object[key].list)
        }
      }

      function getRandomElementValue(array) {
        const index = Math.floor(Math.random() * array.length);
        return array[index].value;
      }
    },
    startScenario(){

      //send scenario to ai

      this.close()
    },
  }
};
</script>

<style scoped>
.footer{
  position: absolute;
  top: 20px;
  right: 15px;
  display: flex;
  justify-content: flex-end;
  text-align: right;
}
.scrollable{
  max-height: 60vh;
  overflow-x: auto;
}
.overlay{
  z-index: 15;
  width: calc(100% - 16.6666% + 24px);
  margin-left: calc(16.6666% - 12px);
}
.section{
  position: relative;
  display: flex;
  width: 100%;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  margin-top: 30px;
}
h3{
  margin-top: 15px;
  margin-bottom: 15px;
  text-align: left;
  width: 75%;
}
.line{
  display: flex;
  gap: 15px;
  justify-content: space-between;
  width: 100%;
  align-items: center;
}
label{
  text-align: center;
  width: 40%;
}
input{
  width: 60%;
}
select{
  width: 60%;
}
option{
  width: inherit !important;
}
</style>
