<script setup>
import { api } from "src/boot/axios";
import { useModelWrapper } from "src/utils/modelWrapper";
import { ref, onMounted } from "vue";

const loading = ref(false);
const urls = ref([]);

const props = defineProps({
  value: String,
});

const emits = defineEmits(["update:value"]);

const value = useModelWrapper(props, emits, "value");

const getUrls = async () => {
  loading.value = true;
  const { data } = await api.get("/urls");
  urls.value = data.urls;
  value.value = data.urls[0];
  loading.value = false;
};

onMounted(async () => {
  await getUrls();
});
</script>

<template>
  <q-list>
    <q-item>
      <q-select
        v-model="value"
        outlined
        :options="urls"
        style="width: 100%"
        dense
        square
        bg-color="white"
        :loading="loading"
        label="Vector URL"
      />
    </q-item>
    <q-separator inset />
  </q-list>
</template>
