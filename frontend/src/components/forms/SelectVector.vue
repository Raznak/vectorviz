<script setup>
import { api } from "src/boot/axios";
import { useModelWrapper } from "src/utils/modelWrapper";
import { computed, ref, onMounted } from "vue";

const loading = ref(false);
const urls = ref([]);

const props = defineProps({
  value: String,
});

const emits = defineEmits(["update:value"]);

const value = useModelWrapper(props, emits, "value");

const normalizeOptions = (items) => {
  if (!items || items.length === 0) return [];
  if (typeof items[0] === "string") {
    return items.map((url) => ({ name: url, url }));
  }
  return items.map((item) => ({
    name: item.name || item.url,
    url: item.url,
  }));
};

const getUrls = async () => {
  loading.value = true;
  const { data } = await api.get("/urls");
  urls.value = normalizeOptions(data.urls);
  value.value = urls.value[0]?.url || "";
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
        option-label="name"
        option-value="url"
        emit-value
        map-options
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
