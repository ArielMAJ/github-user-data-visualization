<template>
  <div id="app">
    <v-container>
      <v-row no-gutters alignContent="center" justify="space-between">
        <v-col md="4">
          <PlotlyChart :propData="plotInfo" divId="plot1" />
        </v-col>
        <v-col md="4">
          <PlotlyChart :propData="plotInfo" divId="plot2" />
        </v-col>
        <v-col md="4">
          <PlotlyChart :propData="plotInfo" divId="plot3" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
import PlotlyChart from "./components/PlotlyChart.vue";

export default {
  name: "app",
  components: {
    PlotlyChart,
  },
  data: function () {
    return {
      plotInfo: {
        data: null,
      },
      loadingData: true,
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        this.loadingData = true;
        const response = await fetch(
          process.env.VUE_APP_BACKEND_ROOT_ENDPOINT + "ArielMAJ/repos"
        );
        const data = await response.json();
        this.plotInfo.data = data.forks;
        console.log(this.plotInfo.data);
        this.loadingData = false;
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
  background-color: bisque;
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
</style>
