from dataclasses import dataclass
from enum import Enum
from uuid import uuid4


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

    def __post_init__(self):
        if not self.session_id:
            self.session_id = str(uuid4())
    def start(
        self,
        timestamp: str,
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
    def resume(
        self,
        timestamp: str,
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
    def pause(
        self,
        timestamp: str,
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
    def end(
        self,
        timestamp: str,
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