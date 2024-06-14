<script setup>
import { api } from "src/boot/axios";
import { nextTick, ref, watch } from "vue";
import { Position } from "@vue-flow/core";
import SidebarStatus from "src/components/SidebarStatus.vue";
import { useQuasar } from "quasar";
import HeaderComp from "src/components/HeaderComp.vue";
import SelectVector from "src/components/forms/SelectVector.vue";

import GraphComp from "src/components/GraphComp.vue";

const $q = useQuasar();
const loading = ref(false);
const health = ref(false);
const meta = ref({});
const hostMetrics = ref({});
const nodes = ref([]);
const edges = ref([]);
const selectedUrl = ref("");
let notify = null;

const style = ref(null);

const getStyle = () => {
  const elem = document.getElementById("colGraph");
  style.value = {
    width: `${elem.offsetWidth}px`,
    height: `${elem.offsetHeight}px`,
  };
};

const fetchGraph = async () => {
  loading.value = true;
  const params = {
    url: selectedUrl.value,
  };

  const { data } = await api.get("/query", { params });
  meta.value = data.meta;
  hostMetrics.value = data.hostMetrics;

  for (const tmp_node of data.nodes) {
    let tmp = {
      id: tmp_node.id,
      label: tmp_node.label,
      type: tmp_node.type,
      events: tmp_node.metrics,
      position: { x: Math.random() * 400, y: Math.random() * 400 },
    };

    if (tmp_node.type === "sources") {
      tmp.class = "node-sources";
      tmp.sourcePosition = Position.Right;
      tmp.targetPosition = Position.Right;
    } else if (tmp_node.type === "transforms") {
      tmp.class = "node-transforms";
      tmp.sourcePosition = Position.Right;
      tmp.targetPosition = Position.Left;
    } else if (tmp_node.type === "sinks") {
      tmp.class = "node-sinks";
      tmp.targetPosition = Position.Left;
      tmp.sourcePosition = Position.Left;
    }

    nodes.value.push(tmp);
  }

  for (const tmp of data.edges) {
    edges.value.push({
      ...tmp,
    });
  }

  if (!style.value) {
    nextTick(() => {
      getStyle();
    });
  }

  setTimeout(async () => {
    await load();
  }, 60000);
};

const fetchHealth = async () => {
  const params = {
    url: selectedUrl.value,
  };

  const { data } = await api.get("/health", { params });
  health.value = data;
};

const load = async () => {
  if (notify) {
    notify();
    notify = null;
  }

  nodes.value = [];
  edges.value = [];
  meta.value = {};
  health.value = false;
  hostMetrics.value = {};

  if (!selectedUrl.value) {
    return;
  }

  try {
    loading.value = true;
    await fetchHealth();
    await fetchGraph();
  } catch (err) {
    notify = $q.notify({
      message: err.response.data.detail,
      type: "negative",
      position: "top",
      timeout: 2000,
    });
  } finally {
    loading.value = false;
  }
};

watch(selectedUrl, async () => {
  await load();
});
</script>

<template>
  <q-layout view="lHh lpR fFf">
    <HeaderComp />

    <q-drawer show-if-above side="left" class="bg-primary">
      <q-toolbar class="bg-primary text-white">
        <q-avatar class="q-mr-sm">
          <img
            src="https://avatars.githubusercontent.com/u/16866914?s=200&v=4"
          />
        </q-avatar>
        VectorViz
      </q-toolbar>

      <q-separator inset />

      <SelectVector v-model:value="selectedUrl" />

      <SidebarStatus
        :health="health"
        :meta="meta"
        :hostMetrics="hostMetrics"
        :loading="loading"
      />
    </q-drawer>
    <q-page-container>
      <q-page>
        <div class="row" :style="`height: ${$q.screen.height - 40}px`">
          <div class="col" id="colGraph" v-if="nodes.length > 0">
            <div v-if="style" :style="style">
              <GraphComp :tmp_nodes="nodes" :tmp_edges="edges" />
            </div>
          </div>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>
