<template>
  <div class="app justify-center">
    <!-- <v-responsive class="mx-auto" max-width="344"> -->
    <v-responsive id="search-bar" max-width="700">
      <v-text-field
        v-model="username"
        label="Search for a GitHub username"
        hint="Write a GitHub username to visualize their account information"
        placeholder="ArielMAJ"
        clearable
        clear-icon="mdi-close-circle"
        type="text"
        variant="solo-filled"
        @keyup.enter="
          pressedEnter = true;
          search();
        "
        @click:clear="cardOpen = false"
      >
      </v-text-field>
    </v-responsive>
    <UserCard
      :username="this.username"
      :reload-watcher="this.reloadCount"
      :exampleUsernames="this.exampleUsernames"
      v-if="cardOpen"
    />
    <v-responsive v-else max-width="1000" class="mx-auto">
      <h3 class="text-center">Or choose one of the following</h3>
      <v-chip-group class="justify-center">
        <v-chip
          v-for="exampleUsername in exampleUsernames"
          :key="exampleUsername"
          @click="
            clickedFastSearch = true;
            username = exampleUsername;
            search();
          "
        >
          {{ exampleUsername }}
        </v-chip>
      </v-chip-group>
    </v-responsive>
  </div>
</template>
<script>
import UserCard from "./components/UserCard.vue";
import _ from "lodash";

export default {
  name: "app",
  components: {
    UserCard,
  },
  data: function () {
    return {
      cardOpen: false,
      username: "",
      reloadCount: 0,
      exampleUsernames: new Set([
        "arielmaj",
        "tauanesales",
        "torvalds",
        "octocat",
        "defunkt",
        "wouerner",
        "mojombo",
        "cs50",
      ]),
      clickedFastSearch: false,
      pressedEnter: false,
    };
  },
  methods: {
    search() {
      if (this.username === "" || this.username === null) {
        this.cardOpen = false;
        return;
      }
      this.reloadCount++;
      this.cardOpen = true;
    },
  },
  watch: {
    username: _.debounce(function () {
      if (this.username === "" || this.username === null) {
        this.cardOpen = false;
        return;
      }
      if (this.clickedFastSearch) {
        this.clickedFastSearch = false;
        return;
      }
      if (this.pressedEnter) {
        this.pressedEnter = false;
        return;
      }
      this.search();
    }, 1500),
  },
};
</script>

<style>
.app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  background-color: black;
  min-height: 100vh;
  min-width: 100vw;
  max-width: 100vw;
  margin: 0;
  position: absolute;
}

body {
  scroll-behavior: smooth;
  overflow-x: hidden;
  min-width: 100vw;
  max-width: 100vw;

  margin: 0;
  padding: 0;
}

.justify-center {
  justify-content: center;
}

.flex-row {
  display: flex;
  flex-direction: row;
  justify-content: center;
}

::-webkit-scrollbar {
  display: none;
}

#search-bar {
  margin: auto;
  margin-top: 20px;
}
</style>
