<template>
  <component :is="loadingComponent" />
</template>

<script>
import LoadingDots from "./LoadingDots.vue";
import LoadingHeart from "./LoadingHeart.vue";

export default {
  name: "loading-component",
  components: {
    LoadingDots,
    LoadingHeart,
  },
  props: {
    loadingComponentChoice: {
      type: String,
      default: "Any",
    },
  },
  computed: {
    loadingComponent() {
      switch (this.loadingComponentChoice) {
        case "Dots":
          return LoadingDots;
        case "Heart":
          return LoadingHeart;
        default:
          return this.randomComponentChoice;
      }
    },
    randomComponentChoice() {
      const componentKeys = Object.keys(this.$options.components);
      return componentKeys[Math.floor(Math.random() * componentKeys.length)];
    },
  },
};
</script>

<style scoped></style>
