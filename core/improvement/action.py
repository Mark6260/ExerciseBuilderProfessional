from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class ActionStatus(Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    BLOCKED = "Blocked"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class ActionPriority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


@dataclass
class ImprovementAction:
    """
    Records an authorised action arising from exercise learning.

    Completion of an action does not itself demonstrate that
    the underlying readiness issue has been resolved.
    """

    action_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    title: str = ""
    description: str = ""

    related_recommendation_ids: list[str] = field(
        default_factory=list
    )
    related_finding_ids: list[str] = field(
        default_factory=list
    )
    related_verification_ids: list[str] = field(
        default_factory=list
    )

    owner: str = ""
    priority: ActionPriority = ActionPriority.MEDIUM
    target_date: str = ""

    status: ActionStatus = ActionStatus.NOT_STARTED

    completion_notes: str = ""
    completion_evidence_ids: list[str] = field(
        default_factory=list
    )

    authorised_by: str = ""
    authorised_at: str = ""

    completed_by: str = ""
    completed_at: str = ""

    def add_recommendation_id(self, recommendation_id: str):
        if (
            recommendation_id
            and recommendation_id not in self.related_recommendation_ids
        ):
            self.related_recommendation_ids.append(
                recommendation_id
            )

    def add_finding_id(self, finding_id: str):
        if (
            finding_id
            and finding_id not in self.related_finding_ids
        ):
            self.related_finding_ids.append(finding_id)

    def add_verification_id(self, verification_id: str):
        if (
            verification_id
            and verification_id not in self.related_verification_ids
        ):
            self.related_verification_ids.append(
                verification_id
            )

    def add_completion_evidence_id(self, evidence_id: str):
        if (
            evidence_id
            and evidence_id not in self.completion_evidence_ids
        ):
            self.completion_evidence_ids.append(evidence_id)

    def mark_authorised_now(self):
        self.authorised_at = datetime.now().isoformat(
            timespec="seconds"
        )

    def mark_completed_now(self):
        self.completed_at = datetime.now().isoformat(
            timespec="seconds"
        )
