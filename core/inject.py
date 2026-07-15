from dataclasses import dataclass, field
from enum import Enum


class InjectStatus(Enum):
    PLANNED = "Planned"
    READY = "Ready"
    ISSUED = "Issued"
    RESPONSE_RECEIVED = "Response Received"
    CLOSED = "Closed"
    WITHDRAWN = "Withdrawn"


@dataclass
class Inject:
    number: int = 0
    title: str = ""
    exercise_time: str = ""
    phase: str = ""
    source: str = ""
    method: str = ""
    audience: str = ""
    category: str = ""

    inject_text: str = ""
    expected_action: str = ""
    facilitator_notes: str = ""

    attachments: list[str] = field(default_factory=list)

    status: InjectStatus = InjectStatus.PLANNED

    def advance(self):
        """Move the inject to the next logical lifecycle state."""

        if self.status == InjectStatus.PLANNED:
            self.status = InjectStatus.READY

        elif self.status == InjectStatus.READY:
            self.status = InjectStatus.ISSUED

        elif self.status == InjectStatus.ISSUED:
            self.status = InjectStatus.RESPONSE_RECEIVED

        elif self.status == InjectStatus.RESPONSE_RECEIVED:
            self.status = InjectStatus.CLOSED

    def withdraw(self):
        """Withdraw an inject from the exercise."""

        if self.status != InjectStatus.CLOSED:
            self.status = InjectStatus.WITHDRAWN

    @property
    def can_advance(self):
        return self.status in (
            InjectStatus.PLANNED,
            InjectStatus.READY,
            InjectStatus.ISSUED,
            InjectStatus.RESPONSE_RECEIVED,
        )

    @property
    def next_action(self):
        actions = {
            InjectStatus.PLANNED: "Make Ready",
            InjectStatus.READY: "Issue Inject",
            InjectStatus.ISSUED: "Record Response",
            InjectStatus.RESPONSE_RECEIVED: "Close Inject",
            InjectStatus.CLOSED: "",
            InjectStatus.WITHDRAWN: "",
        }

        return actions[self.status]

    def __str__(self):
        if self.title:
            return f"{self.number}. {self.title}"

        return f"Inject {self.number}"