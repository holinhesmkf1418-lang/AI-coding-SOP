import { defineStore } from 'pinia'
import { STORE_IDS } from '../../types'
import type { ModelConfig } from '../../types'

export interface ModelState {
  modelConfigs: ModelConfig[]
}

export const useModelStore = defineStore(STORE_IDS.model, {
  state: (): ModelState => ({
    modelConfigs: [],
  }),
})
