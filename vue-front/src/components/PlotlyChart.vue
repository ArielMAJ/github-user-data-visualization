<template>
  <div
    class="plotly-chart"
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
    propData: {
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
  },
  data: function () {
    return {};
  },
  mounted() {
    this.newPlot();
    this.bindEvents();
  },
  created() {
    this.$watch("propData", this.update, { deep: true });
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
      Plotly.newPlot(this.divId, this.propData.data, {
        paper_bgcolor: "transparent",
      });
    },
    update() {
      Plotly.react(this.divId, this.propData.data, {
        paper_bgcolor: "transparent",
      });
    },
  },
};
</script>

<style scoped>
.plotly-chart {
  /* margin: 20px auto; */
  border: 1px solid #ccc;
  border-radius: 50px;
  background-color: transparent;
}
</style>
