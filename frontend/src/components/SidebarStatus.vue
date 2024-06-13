<script setup>
import { humanFileSize } from "src/utils/utils";

const props = defineProps(["health", "meta", "hostMetrics", "loading"]);
</script>

<template>
  <span v-if="!loading">
    <q-list dense dark>
      <q-item-label header class="q-py-sm text-bold">Health</q-item-label>
      <q-item>
        <q-item-section> Status: </q-item-section>
        <q-item-section side>
          <q-chip
            size="md"
            class="float-right text-white"
            square
            dense
            dark
            :color="health.ok ? 'green-8' : 'red-8'"
          >
            {{ health.ok ? "OK" : "KO" }}
          </q-chip>
        </q-item-section>
      </q-item>
      <q-item v-if="meta.version">
        <q-item-section> Version: </q-item-section>
        <q-item-section side>
          <q-chip square color="blue-grey-1" class="text-primary" dense>
            {{ meta.version }}
          </q-chip>
        </q-item-section>
      </q-item>
    </q-list>
    <q-list v-if="hostMetrics.memory" dense dark>
      <q-separator inset class="q-mt-xs" />
      <q-item-label header class="q-py-sm text-bold">Memory</q-item-label>
      <q-item>
        <q-item-section> Used: </q-item-section>
        <q-item-section side>
          <q-chip square color="blue-grey-1" class="text-primary" dense>
            {{ humanFileSize(hostMetrics.memory.usedBytes) }}
          </q-chip>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section> Free: </q-item-section>
        <q-item-section side>
          <q-chip square color="blue-grey-1" class="text-primary" dense>
            {{ humanFileSize(hostMetrics.memory.freeBytes) }}
          </q-chip>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section> Total: </q-item-section>
        <q-item-section side>
          <q-chip square color="blue-grey-1" class="text-primary" dense>
            {{ humanFileSize(hostMetrics.memory.totalBytes) }}
          </q-chip>
        </q-item-section>
      </q-item>
    </q-list>
    <q-list v-if="hostMetrics.swap" dense dark>
      <q-separator inset class="q-mt-xs" />
      <q-item-label header class="q-py-sm text-bold">SWAP</q-item-label>
      <q-item>
        <q-item-section> Used: </q-item-section>
        <q-item-section side>
          <q-chip square color="blue-grey-1" class="text-primary" dense>
            {{ humanFileSize(hostMetrics.swap.usedBytes) }}
          </q-chip>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section> Free: </q-item-section>
        <q-item-section side>
          <q-chip square color="blue-grey-1" class="text-primary" dense>
            {{ humanFileSize(hostMetrics.swap.freeBytes) }}
          </q-chip>
        </q-item-section>
      </q-item>
    </q-list>
    <q-list v-if="hostMetrics.filesystem" dense dark>
      <q-separator inset class="q-mt-xs" />
      <q-item-label header class="q-py-sm text-bold">Filesystem</q-item-label>
      <q-item>
        <q-item-section> Used: </q-item-section>
        <q-item-section side>
          <q-chip square color="blue-grey-1" class="text-primary" dense>
            {{ humanFileSize(hostMetrics.filesystem.usedBytes) }}
          </q-chip>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section> Free: </q-item-section>
        <q-item-section side>
          <q-chip square color="blue-grey-1" class="text-primary" dense>
            {{ humanFileSize(hostMetrics.filesystem.freeBytes) }}
          </q-chip>
        </q-item-section>
      </q-item>
    </q-list>
    <q-list v-if="hostMetrics.loadAverage" dense dark>
      <q-separator inset class="q-mt-xs" />
      <q-item-label header class="q-py-sm text-bold">Load</q-item-label>
      <q-item>
        <q-item-section> Load1: </q-item-section>
        <q-item-section side>
          <q-chip square color="blue-grey-1" class="text-primary" dense>
            {{ parseFloat(hostMetrics.loadAverage.load1).toFixed(2) }}
          </q-chip>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section> Load5: </q-item-section>
        <q-item-section side>
          <q-chip square color="blue-grey-1" class="text-primary" dense>
            {{ parseFloat(hostMetrics.loadAverage.load5).toFixed(2) }}
          </q-chip>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section> Load15: </q-item-section>
        <q-item-section side>
          <q-chip square color="blue-grey-1" class="text-primary" dense>
            {{ parseFloat(hostMetrics.loadAverage.load15).toFixed(2) }}
          </q-chip>
        </q-item-section>
      </q-item>
      <q-separator inset class="q-mt-xs" />
    </q-list>
  </span>
  <q-inner-loading :showing="loading">
    <q-spinner-cube size="50px" color="primary" />
  </q-inner-loading>
</template>
