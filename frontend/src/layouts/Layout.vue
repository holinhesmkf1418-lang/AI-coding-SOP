<script setup lang="ts">
import { layoutNavigationItems } from '../config/layoutNavigation'
</script>

<template>
  <el-container class="app-layout">
    <el-aside class="app-layout__aside" width="240px">
      <div class="app-layout__brand">AI 编程 SOP</div>
      <el-menu class="app-layout__menu" router>
        <el-menu-item
          v-for="item in layoutNavigationItems"
          :key="item.key"
          :index="item.key"
          :route="item.to"
        >
          {{ item.label }}
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-main class="app-layout__main">
      <RouterView />
    </el-main>
  </el-container>
</template>

<style scoped>
.app-layout {
  min-height: 100vh;
  background: #f5f7fa;
}

.app-layout__aside {
  border-right: 1px solid #e4e7ed;
  background: #ffffff;
}

.app-layout__brand {
  display: flex;
  align-items: center;
  height: 64px;
  padding: 0 20px;
  border-bottom: 1px solid #e4e7ed;
  color: #1f2937;
  font-size: 18px;
  font-weight: 600;
}

.app-layout__menu {
  border-right: 0;
}

.app-layout__main {
  min-width: 0;
  padding: 24px;
}
</style>
