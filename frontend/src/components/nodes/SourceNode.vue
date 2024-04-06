<script setup>
import { Handle, Position } from "@vue-flow/core";

const props = defineProps({
  node: {
    type: Object,
    required: true,
  },
});
</script>

<template>
  <div class="text-center q-px-xs">
    <p class="q-ma-none">Source: {{ node.label }}</p>
    <p class="text-bold q-ma-none">
      {{ node.events.receivedEventsTotal.receivedEventsTotal }} Events
    </p>
  </div>

  <Handle id="a" type="source" :position="Position.Right" />
</template>
