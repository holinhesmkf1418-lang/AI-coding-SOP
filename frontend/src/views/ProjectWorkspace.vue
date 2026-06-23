<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <section class="view-placeholder">
    <h1>项目工作台</h1>
    <p>当前项目 ID：{{ route.params.id }}</p>
  </section>
</template>

<style scoped>
.view-placeholder {
  display: grid;
  gap: 8px;
}

.view-placeholder h1 {
  margin: 0;
  color: #1f2937;
  font-size: 24px;
  font-weight: 600;
}

.view-placeholder p {
  margin: 0;
  color: #606266;
}
</style>
