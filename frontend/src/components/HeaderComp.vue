<script setup>
import { useRoute } from "vue-router";

const route = useRoute();
</script>

<template>
  <q-header elevated class="bg-white text-primary">
    <q-toolbar>
      <router-link :to="{ name: 'Home' }">
        <q-btn
          flat
          label="Home"
          color="primary"
          :class="[
            route.name === 'Home' ? 'text-underline' : '',
            'text-subtitle1 text-weight-medium',
          ]"
        />
      </router-link>
      <router-link :to="{ name: 'VRL' }">
        <q-btn
          flat
          label="VRL"
          color="primary"
          :class="[
            route.name === 'VRL' ? 'text-underline' : '',
            'text-subtitle1 text-weight-medium',
          ]"
        />
      </router-link>
    </q-toolbar>
  </q-header>
</template>
