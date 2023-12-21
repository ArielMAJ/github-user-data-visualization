<template>
  <div
    ref="container"
    :id="divId"
    :style="{
      height: height,
      width: width,
    }"
  ></div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";

export default {
  name: "Plotly-Chart",
  props: {
    chartData: {
      type: Object,
      required: true,
    },
    divId: {
      type: String,
      required: true,
    },
    height: {
      type: String,
      default: "350px",
    },
    width: {
      type: String,
      default: "100%",
    },
    layout: {
      default: {
        paper_bgcolor: "transparent",
      },
    },
    config: {
      default: {
        responsive: true,
      },
    },
  },
  data: function () {
    return {};
  },
  mounted() {
    console.log(this.divId, this.chartData)
    this.newPlot();
    this.bindEvents();
  },
  created() {
    this.$watch("chartData", this.update, { deep: true });
  },
  beforeUnmount() {
    this.unbindEvents();
  },
  computed: {
    plotDiv() {
      return this.$refs.container;
    },
  },
  methods: {
    bindEvents() {
      this.plotDiv.on("plotly_redraw", this.redraw);
    },
    unbindEvents() {
      if (!this.plotDiv["off"]) return;
      this.plotDiv.off("plotly_redraw", this.redraw);
    },

    // Redraw in plotly is a plot level event,
    // so all that's published out is the plot's divId
    redraw() {
      this.$emit("redraw", this.divId);
    },

    newPlot() {
      Plotly.newPlot(
        this.divId,
        this.chartData,
        this.layout,
        this.config
      );
    },
    update() {
      Plotly.react(
        this.divId,
        this.chartData,
        this.layout,
        this.config
      );
    },
  },
};
</script>

<style scoped></style>
