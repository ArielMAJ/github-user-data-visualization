<template>
  <div id="app">
    <v-row no-gutters>
      <v-col class="plotly-chart center-content">
        <Loading v-if="plotInfo1.data === null" />
        <PlotlyChart v-else :propData="plotInfo1" divId="plot1" />
      </v-col>
      <v-col class="plotly-chart center-content">
        <LoadingHeart v-if="plotInfo2.data === null" />
        <PlotlyChart v-else :propData="plotInfo2" divId="plot2" />
      </v-col>
      <v-col class="plotly-chart center-content">
        <Loading v-if="plotInfo3.data === null" />
        <PlotlyChart v-else :propData="plotInfo3" divId="plot3" />
      </v-col>
    </v-row>
  </div>
</template>
<script>
import Loading from "./components/Loading.vue";
import LoadingHeart from "./components/LoadingHeart.vue";
import PlotlyChart from "./components/PlotlyChart.vue";

export default {
  name: "app",
  components: {
    PlotlyChart,
    Loading,
    LoadingHeart,
  },
  data: function () {
    const plotData = {
      layout: {
        paper_bgcolor: "transparent",
      },
      config: {
        responsive: true,
      },
    };
    return {
      plotInfo1: {
        data: null,
        ...plotData,
      },
      plotInfo2: {
        data: null,
        ...plotData,
      },
      plotInfo3: {
        data: null,
        ...plotData,
      },
    };
  },
  async mounted() {
    try {
      this.fetchData("a")
        .then((data) => data.json())
        .then((json) => (this.plotInfo1.data = json.forks));
      this.fetchData("b")
        .then((data) => data.json())
        .then((json) => (this.plotInfo2.data = json.forks));
      this.fetchData("c")
        .then((data) => data.json())
        .then((json) => (this.plotInfo3.data = json.forks));
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  },
  methods: {
    async fetchData(username) {
      try {
        console.log(
          "Fetching data...",
          process.env.VUE_APP_BACKEND_ROOT_ENDPOINT + `${username}/repos`
        );
        return fetch(
          process.env.VUE_APP_BACKEND_ROOT_ENDPOINT + `${username}/repos`
        );
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
}

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: black;
  min-height: 100vh;
  min-width: 100vw;
  max-width: 100vw;
}

body {
  scroll-behavior: smooth;
  overflow-x: hidden;
  min-width: 100vw;
  max-width: 100vw;
}

.plotly-chart {
  margin: 20px;
  border: 1px solid #ccc;
  border-radius: 50px;
  background-color: transparent;
  height: 350px;
  min-width: 350px;
  max-width: 45%;
}

.center-content {
  display: flex;
  align-items: center;
  justify-content: center;
}

::-webkit-scrollbar {
  display: none;
}
</style>
