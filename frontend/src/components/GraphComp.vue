<script setup>
import { ref, nextTick } from "vue";
import { VueFlow, useVueFlow } from "@vue-flow/core";
import { Background } from "@vue-flow/background";
import { ControlButton, Controls } from "@vue-flow/controls";
import { useLayout } from "../utils/useLayout";
import SourceNode from "./nodes/SourceNode.vue";
import SinkNode from "./nodes/SinkNode.vue";
import TransformNode from "./nodes/TransformNode.vue";
import IconComp from "./IconComp.vue";

const { layout } = useLayout();
/**
 * useVueFlow provides all event handlers and store properties
 * You can pass the composable an object that has the same properties as the VueFlow component props
 */

const props = defineProps({
  tmp_nodes: {
    type: Array,
  },
  tmp_edges: {
    type: Array,
  },
});

const nodes = ref(props.tmp_nodes);
const edges = ref(props.tmp_edges);
const { onPaneReady } = useVueFlow();

// our dark mode toggle flag
const dark = ref(false);

/**
 * This is a Vue Flow event-hook which can be listened to from anywhere you call the composable, instead of only on the main component
 * Any event that is available as `@event-name` on the VueFlow component is also available as `onEventName` on the composable and vice versa
 *
 * onPaneReady is called when viewpane & nodes have visible dimensions
 */
onPaneReady(({ fitView }) => {
  nodes.value = layout(nodes.value, edges.value, "LR");

  nextTick(() => {
    fitView();
  });
});

function toggleDarkMode() {
  dark.value = !dark.value;
}
</script>

<template>
  <VueFlow
    :nodes="nodes"
    :edges="edges"
    :class="{ dark }"
    class="basicflow"
    :default-viewport="{ zoom: 0.2 }"
    :min-zoom="0.2"
    :max-zoom="4"
  >
    <Background pattern-color="#aaa" :gap="16" />

    <template #node-sources="node">
      <SourceNode :node="node" />
    </template>

    <template #node-transforms="node">
      <TransformNode :node="node" />
    </template>

    <template #node-sinks="node">
      <SinkNode :node="node" />
    </template>

    <Controls position="top-right">
      <ControlButton title="Toggle Dark Mode" @click="toggleDarkMode">
        <IconComp v-if="dark" name="sun" />
        <IconComp v-else name="moon" />
      </ControlButton>
    </Controls>
  </VueFlow>
</template>
