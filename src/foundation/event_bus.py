from typing import Any

class EventBus:
    """
    Architectural Principle: Event-Driven Extensibility.
    An internal EventBus manages system integrations. Event subscribers
    hook into pipeline milestones without code changes in the orchestrator.
    """
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type: str, callback_fn):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback_fn)

    def publish(self, event_type: str, data: Any = None):
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error in EventBus subscriber for event '{event_type}': {e}")
