from fastapi_events.handlers.local import local_handler
from fastapi_events.typing import Event

def handle_event(event: Event):
    print(f"Received event: {event}")

local_handler.register(event_name="example_event", callback=handle_event)