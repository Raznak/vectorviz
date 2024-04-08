<script setup>
import { api } from "src/boot/axios";
import { nextTick, onMounted, ref } from "vue";
import { Position } from "@vue-flow/core";
import { humanFileSize } from "src/utils/utils";

import { useQuasar } from "quasar";

import GraphComp from "src/components/GraphComp.vue";

const $q = useQuasar();
const loading = ref(false);
const health = ref(false);
const meta = ref({});
const hostMetrics = ref({});
const urls = ref([]);
const selectedUrl = ref("");
const nodes = ref([]);
const edges = ref([]);

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

  nodes.value = [];
  edges.value = [];

  try {
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
  } catch (err) {
    $q.notify({
      message: err.response.data.detail,
      type: "negative",
      position: "top",
      timeout: 2000,
    });
  } finally {
    loading.value = false;
  }
};

const fetchHealth = async () => {
  const params = {
    url: selectedUrl.value,
  };
  const { data } = await api.get("/health", { params });
  health.value = data;
};

const load = async () => {
  await fetchHealth();
  await fetchGraph();
};

const getUrls = async () => {
  loading.value = true;
  const { data } = await api.get("/urls");
  urls.value = data.urls;
  selectedUrl.value = data.urls[0];
  loading.value = false;
  await load();
};

onMounted(async () => {
  await getUrls();
});
</script>

<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-avatar class="q-mr-lg">
          <img
            src="https://avatars.githubusercontent.com/u/16866914?s=200&v=4"
          />
        </q-avatar>
        <q-select
          v-model="selectedUrl"
          outlined
          :options="urls"
          dense
          filled
          square
          style="width: 30%"
          @update:model-value="load"
          bg-color="white"
          :loading="loading"
          label="Vector URL"
        >
          <template v-slot:after>
            <q-btn color="white" @click="load" dense flat icon="send" />
          </template>
        </q-select>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page>
        <div class="row" :style="`height: ${$q.screen.height - 40}px`">
          <div class="col-2">
            <q-card square dark class="full-height bg-blue-grey-10">
              <q-card-section>
                <q-list dense>
                  <q-item-label header>Health</q-item-label>
                  <q-item>
                    <q-item-section> Status: </q-item-section>
                    <q-item-section side>
                      <q-chip
                        size="md"
                        square
                        dark
                        :color="health.ok ? 'green-8' : 'red-8'"
                      >
                        {{ health.ok ? "OK" : "KO" }}
                      </q-chip>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section> Version: </q-item-section>
                    <q-item-section side>
                      <q-chip square color="primary">
                        {{ meta.version }}
                      </q-chip>
                    </q-item-section>
                  </q-item>
                </q-list>
                <q-list v-if="hostMetrics.memory" dense>
                  <q-item-label header>Memory</q-item-label>
                  <q-item>
                    <q-item-section> Used: </q-item-section>
                    <q-item-section side>
                      <q-chip square color="primary">
                        {{ humanFileSize(hostMetrics.memory.usedBytes) }}
                      </q-chip>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section> Free: </q-item-section>
                    <q-item-section side>
                      <q-chip square color="primary">
                        {{ humanFileSize(hostMetrics.memory.freeBytes) }}
                      </q-chip>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section> Total: </q-item-section>
                    <q-item-section side>
                      <q-chip square color="primary">
                        {{ humanFileSize(hostMetrics.memory.totalBytes) }}
                      </q-chip>
                    </q-item-section>
                  </q-item>
                </q-list>
                <q-list v-if="hostMetrics.swap" dense>
                  <q-item-label header>SWAP</q-item-label>
                  <q-item>
                    <q-item-section> Used: </q-item-section>
                    <q-item-section side>
                      <q-chip square color="primary">
                        {{ humanFileSize(hostMetrics.swap.usedBytes) }}
                      </q-chip>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section> Free: </q-item-section>
                    <q-item-section side>
                      <q-chip square color="primary">
                        {{ humanFileSize(hostMetrics.swap.freeBytes) }}
                      </q-chip>
                    </q-item-section>
                  </q-item>
                </q-list>
                <q-list v-if="hostMetrics.filesystem" dense>
                  <q-item-label header>Filesystem</q-item-label>
                  <q-item>
                    <q-item-section> Used: </q-item-section>
                    <q-item-section side>
                      <q-chip square color="primary">
                        {{ humanFileSize(hostMetrics.filesystem.usedBytes) }}
                      </q-chip>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section> Free: </q-item-section>
                    <q-item-section side>
                      <q-chip square color="primary">
                        {{ humanFileSize(hostMetrics.filesystem.freeBytes) }}
                      </q-chip>
                    </q-item-section>
                  </q-item>
                </q-list>
                <q-list v-if="hostMetrics.loadAverage" dense>
                  <q-item-label header>Load</q-item-label>
                  <q-item>
                    <q-item-section> Load1: </q-item-section>
                    <q-item-section side>
                      <q-chip square color="primary">
                        {{
                          parseFloat(hostMetrics.loadAverage.load1).toFixed(2)
                        }}
                      </q-chip>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section> Load5: </q-item-section>
                    <q-item-section side>
                      <q-chip square color="primary">
                        {{
                          parseFloat(hostMetrics.loadAverage.load5).toFixed(2)
                        }}
                      </q-chip>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section> Load15: </q-item-section>
                    <q-item-section side>
                      <q-chip square color="primary">
                        {{
                          parseFloat(hostMetrics.loadAverage.load15).toFixed(2)
                        }}
                      </q-chip>
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-10" id="colGraph" v-if="nodes.length > 0">
            <div v-if="style" :style="style">
              <GraphComp :tmp_nodes="nodes" :tmp_edges="edges" />
            </div>
          </div>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>
