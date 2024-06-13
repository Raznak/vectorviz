<script setup>
import HeaderComp from "src/components/HeaderComp.vue";
import SelectVector from "src/components/forms/SelectVector.vue";
import { ref } from "vue";

const selectedUrl = ref(null);
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

      <q-separator />
      <SelectVector v-model:value="selectedUrl" />
    </q-drawer>

    <q-page-container>
      <q-page> </q-page>
    </q-page-container>
  </q-layout>
</template>
