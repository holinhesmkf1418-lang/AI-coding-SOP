import { defineStore } from 'pinia'
import { STORE_IDS } from '../../types'
import type { StepConfig, StepOutput } from '../../types'

export interface StepState {
  stepConfigs: StepConfig[]
  stepOutputs: StepOutput[]
}

export const useStepStore = defineStore(STORE_IDS.step, {
  state: (): StepState => ({
    stepConfigs: [],
    stepOutputs: [],
  }),
})
