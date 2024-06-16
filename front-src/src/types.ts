interface Meta {
  type: string
  filename: string
  id: string
}

export interface AssistantContextItem {
  from: 'assistant'
  data: string
  metadata: Meta[]
  success: boolean
  inquiryContent?: string
}

export interface UserContextItem {
  from: 'user'
  data: string
}

export type ContextItem = AssistantContextItem | UserContextItem
