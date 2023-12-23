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
        type="text"
        variant="solo-filled"
        :rules="[rules.required]"
        @keyup.enter="search"
      >
      </v-text-field>
    </v-responsive>
    <!-- <v-btn
      class="white--text"
      color="primary"
      @click="pieChartModalOpen = !pieChartModalOpen"
    >Open Repository Visualization
    </v-btn> -->
    <PieChartModal
      v-if="pieChartModalOpen"
      :username="this.username"
      :reload-watcher="this.reloadCount"
    />
  </div>
</template>
<script>
import PieChartModal from "./modals/PieChartModal.vue";
import _ from "lodash";

export default {
  name: "app",
  components: {
    PieChartModal,
  },
  data: function () {
    return {
      pieChartModalOpen: false,
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
        this.pieChartModalOpen = true;
      }
    },
  },
  watch: {
    username: _.debounce(function () {
      if (this.username === "" || this.username === null) {
        this.pieChartModalOpen = false;
      }
    }, 2000),
  },
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
}

.app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: rgb(4, 162, 4);
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
