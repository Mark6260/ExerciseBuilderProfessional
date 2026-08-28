from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class ActualTimelineEntryType(Enum):
    SESSION_CONTROL = "Session Control"
    INJECT_CONTROL = "Inject Control"
    DELIVERY_ACTIVITY = "Delivery Activity"


@dataclass
class ActualTimelineEntry:
    timestamp: str
    entry_type: ActualTimelineEntryType
    summary: str

    entry_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    source_id: str = ""
    inject_number: int | None = None

    actor: str = ""
    rationale: str = ""