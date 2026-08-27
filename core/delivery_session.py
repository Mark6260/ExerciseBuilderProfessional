from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4

from core.delivery_event import (
    DeliveryEvent,
    DeliveryEventType,
)
from core.live_inject_event import (
    LiveInjectEvent,
    LiveInjectEventType,
)


class DeliverySessionStatus(Enum):
    NOT_STARTED = "Not Started"
    RUNNING = "Running"
    PAUSED = "Paused"
    ENDED = "Ended"


@dataclass
class DeliverySession:
    """
    Represents the live delivery of an exercise.

    The delivery session records the state of exercise
    delivery. It does not itself issue injects or alter
    the planned MEL/MIL.
    """

    session_id: str = ""
    status: DeliverySessionStatus = (
        DeliverySessionStatus.NOT_STARTED
    )

    started_at: str = ""
    paused_at: str = ""
    resumed_at: str = ""
    ended_at: str = ""
    
    events: list = field(
        default_factory=list
    )
    activities: list = field(
        default_factory=list
    )
    live_inject_events: list = field(
        default_factory=list
    )
    live_inject_records: list = field(
        default_factory=list
    )
    
    def __post_init__(self):
        if not self.session_id:
            self.session_id = str(uuid4())
    def add_event(
        self,
        event,
    ):
        self.events.append(event)
    def add_activity(
        self,
        activity,
    ):
        self.activities.append(
            activity
        )
    def add_live_inject_event(
        self,
        event,
    ):
        self.live_inject_events.append(
            event
        )
    def add_live_inject_record(
        self,
        record,
    ):
        self.live_inject_records.append(
            record
        )
    def get_live_inject_record(
        self,
        inject_number: int,
    ):
        for record in self.live_inject_records:
            if (
                record.inject_number
                == inject_number
            ):
                return record

        return None
    
    def hold_live_inject(
        self,
        inject_number: int,
        timestamp: str,
        recorded_by: str = "",
        rationale: str = "",
    ):
        record = self.get_live_inject_record(
            inject_number
        )

        if record is None:
            raise ValueError(
                f"Cannot hold Inject {inject_number}: "
                "no live inject record exists."
            )

        record.hold()

        event = LiveInjectEvent(
            event_type=LiveInjectEventType.HELD,
            inject_number=inject_number,
            timestamp=timestamp,
            recorded_by=recorded_by,
            rationale=rationale,
        )

        self.add_live_inject_event(
            event
        )
    def release_live_inject(
        self,
        inject_number: int,
        timestamp: str,
        recorded_by: str = "",
        rationale: str = "",
    ):
        record = self.get_live_inject_record(
            inject_number
        )

        if record is None:
            raise ValueError(
                f"Cannot release Inject {inject_number}: "
                "no live inject record exists."
            )

        record.release()

        event = LiveInjectEvent(
            event_type=LiveInjectEventType.RELEASED,
            inject_number=inject_number,
            timestamp=timestamp,
            recorded_by=recorded_by,
            rationale=rationale,
        )

        self.add_live_inject_event(
            event
        )
    def delay_live_inject(
        self,
        inject_number: int,
        timestamp: str,
        recorded_by: str = "",
        rationale: str = "",
    ):
        record = self.get_live_inject_record(
            inject_number
        )

        if record is None:
            raise ValueError(
                f"Cannot delay Inject {inject_number}: "
                "no live inject record exists."
            )

        event = LiveInjectEvent(
            event_type=LiveInjectEventType.DELAYED,
            inject_number=inject_number,
            timestamp=timestamp,
            recorded_by=recorded_by,
            rationale=rationale,
        )

        self.add_live_inject_event(
            event
        )
    def bring_forward_live_inject(
        self,
        inject_number: int,
        timestamp: str,
        recorded_by: str = "",
        rationale: str = "",
    ):
        record = self.get_live_inject_record(
            inject_number
        )

        if record is None:
            raise ValueError(
                f"Cannot bring forward Inject {inject_number}: "
                "no live inject record exists."
            )

        event = LiveInjectEvent(
            event_type=(
                LiveInjectEventType.BROUGHT_FORWARD
            ),
            inject_number=inject_number,
            timestamp=timestamp,
            recorded_by=recorded_by,
            rationale=rationale,
        )

        self.add_live_inject_event(
            event
        )
    def amend_live_inject_for_delivery(
        self,
        inject_number: int,
        timestamp: str,
        original_content: str,
        resulting_content: str,
        recorded_by: str = "",
        rationale: str = "",
    ):
        record = self.get_live_inject_record(
            inject_number
        )

        if record is None:
            raise ValueError(
                f"Cannot amend Inject {inject_number}: "
                "no live inject record exists."
            )

        original_content = (
            original_content.strip()
        )
        resulting_content = (
            resulting_content.strip()
        )

        if not resulting_content:
            raise ValueError(
                "Amended delivery content cannot be empty."
            )

        record.delivery_content = (
            resulting_content
        )

        event = LiveInjectEvent(
            event_type=(
                LiveInjectEventType.AMENDED_FOR_DELIVERY
            ),
            inject_number=inject_number,
            timestamp=timestamp,
            recorded_by=recorded_by,
            rationale=rationale,
            original_content=original_content,
            resulting_content=resulting_content,
        )

        self.add_live_inject_event(
            event
        )   
    def start(
        self,
        timestamp: str,
        recorded_by: str = "",
    ):
        if (
            self.status
            is not DeliverySessionStatus.NOT_STARTED
        ):
            raise ValueError(
                "Delivery session can only be started "
                "when its status is Not Started."
            )

        self.started_at = timestamp
        self.status = (
            DeliverySessionStatus.RUNNING
        )

        self.add_event(
            DeliveryEvent(
                event_type=(
                    DeliveryEventType.SESSION_STARTED
                ),
                timestamp=timestamp,
                recorded_by=recorded_by,
            )
        )
    def resume(
        self,
        timestamp: str,
        recorded_by: str = "",
        rationale: str = "",
    ):
        if (
            self.status
            is not DeliverySessionStatus.PAUSED
        ):
            raise ValueError(
                "Delivery session can only be resumed "
                "while it is Paused."
            )

        self.resumed_at = timestamp
        self.status = (
            DeliverySessionStatus.RUNNING
        )

        self.add_event(
            DeliveryEvent(
                event_type=(
                    DeliveryEventType.SESSION_RESUMED
                ),
                timestamp=timestamp,
                recorded_by=recorded_by,
                rationale=rationale,
            )
        )
    def pause(
        self,
        timestamp: str,
        recorded_by: str = "",
        rationale: str = "",
    ):
        if (
            self.status
            is not DeliverySessionStatus.RUNNING
        ):
            raise ValueError(
                "Delivery session can only be paused "
                "while it is Running."
            )

        self.paused_at = timestamp
        self.status = (
            DeliverySessionStatus.PAUSED
        )

        self.add_event(
            DeliveryEvent(
                event_type=(
                    DeliveryEventType.SESSION_PAUSED
                ),
                timestamp=timestamp,
                recorded_by=recorded_by,
                rationale=rationale,
            )
        )
    def end(
        self,
        timestamp: str,
        recorded_by: str = "",
        rationale: str = "",
    ):
        if self.status not in (
            DeliverySessionStatus.RUNNING,
            DeliverySessionStatus.PAUSED,
        ):
            raise ValueError(
                "Delivery session can only be ended "
                "while it is Running or Paused."
            )

        self.ended_at = timestamp
        self.status = (
            DeliverySessionStatus.ENDED
        )

        self.add_event(
            DeliveryEvent(
                event_type=(
                    DeliveryEventType.SESSION_ENDED
                ),
                timestamp=timestamp,
                recorded_by=recorded_by,
                rationale=rationale,
            )
        )