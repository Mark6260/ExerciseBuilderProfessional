from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class LiveInjectStatus(Enum):
    PENDING = "Pending"
    READY = "Ready"
    ACTIVE = "Active"
    CLOSED = "Closed"
    SKIPPED = "Skipped"
    WITHDRAWN = "Withdrawn"
    
class LiveInjectControlCondition(Enum):
    NORMAL = "Normal"
    HELD = "Held"


@dataclass
class LiveInjectRecord:
    """
    Represents the live delivery state of one planned inject.

    The planned Inject remains the authoritative design record.
    This object records what happened to that inject during a
    particular delivery session.
    """

    inject_number: int
    planned_time: str = ""
    delivery_content: str = ""

    record_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    status: LiveInjectStatus = (
        LiveInjectStatus.PENDING
    )
    
    control_condition: LiveInjectControlCondition = (
        LiveInjectControlCondition.NORMAL
    )
    
    ready_at: str = ""
    activated_at: str = ""
    closed_at: str = ""

    controlled_by: str = ""
    
    def make_ready(
        self,
        timestamp: str,
        controlled_by: str = "",
    ):
        if (
            self.status
            is not LiveInjectStatus.PENDING
        ):
            raise ValueError(
                "Live inject can only be made ready "
                "while it is Pending."
            )

        self.ready_at = timestamp

        if controlled_by.strip():
            self.controlled_by = (
                controlled_by.strip()
            )

        self.status = (
            LiveInjectStatus.READY
        )
    def activate(
        self,
        timestamp: str,
        controlled_by: str = "",
    ):
        if (
            self.status
            is not LiveInjectStatus.READY
        ):
            raise ValueError(
                "Live inject can only be activated "
                "while it is Ready."
            )
        if (
            self.control_condition
            is LiveInjectControlCondition.HELD
        ):
            raise ValueError(
                "Live inject cannot be activated "
                "while it is Held."
            )    

        self.activated_at = timestamp

        if controlled_by.strip():
            self.controlled_by = (
                controlled_by.strip()
            )

        self.status = (
            LiveInjectStatus.ACTIVE
        )
    def close(
        self,
        timestamp: str,
        controlled_by: str = "",
    ):
        if (
            self.status
            is not LiveInjectStatus.ACTIVE
        ):
            raise ValueError(
                "Live inject can only be closed "
                "while it is Active."
            )

        self.closed_at = timestamp

        if controlled_by.strip():
            self.controlled_by = (
                controlled_by.strip()
            )

        self.status = (
            LiveInjectStatus.CLOSED
        )
    def skip(
        self,
        timestamp: str,
        controlled_by: str = "",
    ):
        if self.status not in (
            LiveInjectStatus.PENDING,
            LiveInjectStatus.READY,
        ):
            raise ValueError(
                "Live inject can only be skipped "
                "while it is Pending or Ready."
            )

        self.closed_at = timestamp

        if controlled_by.strip():
            self.controlled_by = (
                controlled_by.strip()
            )

        self.status = (
            LiveInjectStatus.SKIPPED
        )
    def withdraw(
        self,
        timestamp: str,
        controlled_by: str = "",
    ):
        if self.status not in (
            LiveInjectStatus.PENDING,
            LiveInjectStatus.READY,
        ):
            raise ValueError(
                "Live inject can only be withdrawn "
                "while it is Pending or Ready."
            )

        self.closed_at = timestamp

        if controlled_by.strip():
            self.controlled_by = (
                controlled_by.strip()
            )

        self.status = (
            LiveInjectStatus.WITHDRAWN
        )
    def hold(
        self,
    ):
        if self.status not in (
            LiveInjectStatus.PENDING,
            LiveInjectStatus.READY,
        ):
            raise ValueError(
                "Live inject can only be held "
                "while it is Pending or Ready."
            )

        if (
            self.control_condition
            is LiveInjectControlCondition.HELD
        ):
            raise ValueError(
                "Live inject is already Held."
            )

        self.control_condition = (
            LiveInjectControlCondition.HELD
        )
    def release(
        self,
    ):
        if (
            self.control_condition
            is not LiveInjectControlCondition.HELD
        ):
            raise ValueError(
                "Live inject can only be released "
                "while it is Held."
            )

        if self.status not in (
            LiveInjectStatus.PENDING,
            LiveInjectStatus.READY,
        ):
            raise ValueError(
                "Held live inject can only be released "
                "while it is Pending or Ready."
            )

        self.control_condition = (
            LiveInjectControlCondition.NORMAL
        )