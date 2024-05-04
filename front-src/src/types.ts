export interface AssistantContextItem {
  from: 'assistant'
  data: string
  imageIds: string[]
}

export interface UserContextItem {
  from: 'user'
  data: string
}

export type ContextItem = AssistantContextItem | UserContextItem
