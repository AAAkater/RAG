const _eventNames = ["API_UN_AUTH", "API_INVALID", "API_INTERNAL_SERVER_ERROR"]

type EventNames = (typeof _eventNames)[number]
class EventEmitter {
  private listeners: Record<string, Set<Function>> = {
    API_UN_AUTH: new Set(),
    API_INVALID: new Set(),
    API_INTERNAL_SERVER_ERROR: new Set(),
  }

  on(eventName: EventNames, listener: Function) {
    this.listeners[eventName].add(listener)
  }
  emit(eventName: EventNames, ...args: any[]) {
    this.listeners[eventName].forEach((listener) => {
      listener(...args)
    })
  }
}

const emitter = new EventEmitter()
export { emitter }
