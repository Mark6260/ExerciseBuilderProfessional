from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class LiveInjectEventType(Enum):
    DELAYED = "Delayed"
    BROUGHT_FORWARD = "Brought Forward"
    HELD = "Held"
    RELEASED = "Released"
    AMENDED_FOR_DELIVERY = "Amended for Delivery"


@dataclass
class LiveInjectEvent:
    """
    Records an Exercise Control decision affecting the live
    delivery of a planned inject.

    These events explain how actual delivery differed from
    the planned MEL/MIL without altering the authoritative
    planned inject.
    """

    event_type: LiveInjectEventType
    inject_number: int
    timestamp: str

    event_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    recorded_by: str = ""
    rationale: str = ""

    original_content: str = ""
    resulting_content: str = ""