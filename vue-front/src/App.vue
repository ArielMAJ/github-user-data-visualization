<template>
  <div class="app justify-center">
    <!-- <v-responsive class="mx-auto" max-width="344"> -->
    <v-responsive id="search-bar" max-width="700">
      <v-text-field
        v-model="username"
        label="Search for a GitHub username"
        hint="Write a GitHub username and press enter to visualize their account information"
        placeholder="ArielMAJ"
        clearable
        clear-icon="mdi-close-circle"
        type="text"
        variant="solo-filled"
        :rules="[rules.required]"
        @keyup.enter="search"
        @click:clear="cardOpen = false"
      >
      </v-text-field>
    </v-responsive>
    <UserCard
      :username="this.username"
      :reload-watcher="this.reloadCount"
      v-if="cardOpen"
    />
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
      rules: {
        required: (value) => !!value || "Field is required",
      },
      username: "",
      reloadCount: 0,
    };
  },
  methods: {
    search() {
      if (this.username !== "") {
        this.reloadCount++;
        this.cardOpen = true;
      }
    },
  },
  watch: {
    username: _.debounce(function () {
      if (this.username !== "" && this.username !== null) {
        this.search();
      }
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

::-webkit-scrollbar {
  display: none;
}

#search-bar {
  margin: auto;
  margin-top: 20px;
}
</style>
