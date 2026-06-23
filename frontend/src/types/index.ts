export type EntityId = string
export type DateTimeString = string
export type StepNumber = number
export type ConfigDrivenValue = string
export type NullableText = string | null

export type StepOutputStatus = ConfigDrivenValue
export type ModelProvider = ConfigDrivenValue

export const STORE_IDS = {
  project: 'project',
  step: 'step',
  model: 'model',
} as const

export type StoreId = (typeof STORE_IDS)[keyof typeof STORE_IDS]

export interface Project {
  id: EntityId
  name: string
  description: NullableText
  created_at: DateTimeString
  updated_at: DateTimeString
}

export interface StepConfig {
  id: EntityId
  step_number: StepNumber
  name: string
  description: NullableText
  is_active: boolean
  icon: NullableText
}

export interface StepOutput {
  id: EntityId
  project_id: EntityId
  step_number: StepNumber
  ai_output: string
  edited_output: NullableText
  status: StepOutputStatus
  created_at: DateTimeString
}

export interface ModelConfig {
  id: EntityId
  name: string
  provider: ModelProvider
  api_endpoint: string
  is_active: boolean
}

export interface PromptTemplate {
  id: EntityId
  step_number: StepNumber
  name: string
  content: string
  is_custom: boolean
  is_default: boolean
}
