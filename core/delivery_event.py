from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class DeliveryEventType(Enum):
    SESSION_STARTED = "Session Started"
    SESSION_PAUSED = "Session Paused"
    SESSION_RESUMED = "Session Resumed"
    SESSION_ENDED = "Session Ended"


@dataclass
class DeliveryEvent:
    """
    Records something that happened during live exercise delivery.

    Delivery events are historical records. They do not themselves
    alter the delivery session or the planned MEL/MIL.
    """

    event_type: DeliveryEventType
    timestamp: str

    event_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    recorded_by: str = ""
    rationale: str = ""