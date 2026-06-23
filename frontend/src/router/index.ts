import { createRouter, createWebHistory } from 'vue-router'
import Layout from '../layouts/Layout.vue'
import HomeView from '../views/HomeView.vue'
import ProjectWorkspace from '../views/ProjectWorkspace.vue'
import SettingsView from '../views/SettingsView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: Layout,
      children: [
        {
          path: '',
          name: 'home',
          component: HomeView,
        },
        {
          path: 'project/:id',
          name: 'project-workspace',
          component: ProjectWorkspace,
        },
        {
          path: 'settings',
          name: 'settings',
          component: SettingsView,
        },
      ],
    },
  ],
})

export default router
