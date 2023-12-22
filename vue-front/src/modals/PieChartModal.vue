<template>
  <v-row no-gutters class="justify-center">
    <v-col
      v-bind:key="item"
      v-for="item in plotItems"
      class="plotly-chart center-content"
    >
      <h2 class="margin-up" v-if="item.chartData !== null">
        {{ item.chartData[0].labels[0] }}
      </h2>
      <Loading v-if="item.chartData === null" />
      <PlotlyChart
        v-else
        :chartData="item.chartData"
        :divId="item.information"
      />
    </v-col>
  </v-row>
</template>
<script>
import Loading from "../components/Loading.vue";
import PlotlyChart from "../components/PlotlyChart.vue";

export default {
  name: "pie-chart-modal",
  components: {
    PlotlyChart,
    Loading,
  },
  props: {
    username: {
      type: String,
      required: true,
    },
  },
  data: function () {
    return {
      plotItems: [
        { information: "allow_forking", chartData: null },
        { information: "archived", chartData: null },
        { information: "disabled", chartData: null },
        { information: "fork", chartData: null },
        { information: "has_discussions", chartData: null },
        { information: "has_downloads", chartData: null },
        { information: "has_issues", chartData: null },
        { information: "has_pages", chartData: null },
        { information: "has_projects", chartData: null },
        { information: "has_wiki", chartData: null },
        { information: "is_template", chartData: null },
        { information: "private", chartData: null },
        { information: "web_commit_signoff_required", chartData: null },
      ],
    };
  },
  async mounted() {
    this.plotItems.forEach((item) => {
      this.fetchData(this.username, item);
    });
  },
  methods: {
    async fetchData(username, item) {
      try {
        console.log(
          "Fetching data...",
          process.env.VUE_APP_BACKEND_ROOT_ENDPOINT +
            `${username}/${item.information}`
        );
        const resp = await fetch(
          process.env.VUE_APP_BACKEND_ROOT_ENDPOINT +
            `${username}/${item.information}`
        );
        item.chartData = await resp.json();
        console.log(item);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
};
</script>

<style scoped>
.plotly-chart {
  margin: 20px;
  border: 1px solid #ccc;
  border-radius: 50px;
  background-color: transparent;
  height: 325px;
  min-width: 325px;
  max-width: 40%;
}

.margin-up {
  margin-top: 20px;
}
.center-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
}

.justify-center {
  justify-content: center;
}
</style>
