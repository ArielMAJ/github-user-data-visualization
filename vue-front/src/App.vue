<template>
  <div id="app">
    <v-container>
      <v-row no-gutters justify="space-around">
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
    </v-container>
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
    LoadingHeart
  },
  data: function () {
    return {
      plotInfo1: {
        data: null,
      },
      plotInfo2: {
        data: null,
      },
      plotInfo3: {
        data: null,
      },
    };
  },
  async mounted() {
    try {
      const [data1, data2, data3] = await Promise.all([
        this.fetchData(),
        this.fetchData(),
        this.fetchData(),
      ]);

      this.plotInfo1.data = (await data1.json()).forks;
      this.plotInfo2.data = (await data2.json()).forks;
      this.plotInfo3.data = (await data3.json()).forks;
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  },
  methods: {
    async fetchData() {
      try {
        console.log("Fetching data...");
        return fetch(
          process.env.VUE_APP_BACKEND_ROOT_ENDPOINT + "ArielMAJ/repos"
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
  position: absolute;
}

body {
  scroll-behavior: smooth;
  overflow-y: hidden;
  overflow-x: hidden;
  min-width: 100vw;
  max-width: 100vw;
}

.plotly-chart {
  margin: 20px;
  border: 1px solid #ccc;
  border-radius: 50px;
  background-color: transparent;
}

.center-content {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 350px;
}
</style>
