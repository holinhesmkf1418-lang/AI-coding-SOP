import { defineStore } from 'pinia'
import { STORE_IDS } from '../../types'
import type { Project } from '../../types'

export interface ProjectState {
  projects: Project[]
  currentProject: Project | null
}

export const useProjectStore = defineStore(STORE_IDS.project, {
  state: (): ProjectState => ({
    projects: [],
    currentProject: null,
  }),
})
