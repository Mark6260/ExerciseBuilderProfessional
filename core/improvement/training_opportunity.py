from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class TrainingOpportunityStatus(Enum):
    POTENTIAL = "Potential"
    UNDER_REVIEW = "Under Review"
    VALIDATED = "Validated"
    AGREED = "Agreed"
    COMPLETED = "Completed"
    NOT_SUITABLE = "Not Suitable"
    CANCELLED = "Cancelled"


@dataclass
class TrainingOpportunity:
    """
    Records an existing or proposed training opportunity
    that may help address a finding, recommendation,
    improvement action or assessment requirement.

    Identification of an opportunity does not mean that
    it is suitable or that readiness has been demonstrated.
    """

    opportunity_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    title: str = ""
    organisation: str = ""
    description: str = ""

    start_date: str = ""
    end_date: str = ""
    location: str = ""

    status: TrainingOpportunityStatus = (
        TrainingOpportunityStatus.POTENTIAL
    )

    related_finding_ids: list[str] = field(
        default_factory=list
    )

    related_recommendation_ids: list[str] = field(
        default_factory=list
    )

    related_action_ids: list[str] = field(
        default_factory=list
    )

    suitability_rationale: str = ""

    access_confirmed: bool = False
    assessment_arrangements_confirmed: bool = False

    point_of_contact: str = ""

    identified_by: str = ""
    identified_at: str = ""

    validated_by: str = ""
    validated_at: str = ""

    def add_finding_id(self, finding_id: str):
        if (
            finding_id
            and finding_id not in self.related_finding_ids
        ):
            self.related_finding_ids.append(finding_id)

    def add_recommendation_id(self, recommendation_id: str):
        if (
            recommendation_id
            and recommendation_id
            not in self.related_recommendation_ids
        ):
            self.related_recommendation_ids.append(
                recommendation_id
            )

    def add_action_id(self, action_id: str):
        if (
            action_id
            and action_id not in self.related_action_ids
        ):
            self.related_action_ids.append(action_id)

    def mark_identified_now(self):
        self.identified_at = datetime.now().isoformat(
            timespec="seconds"
        )

    def mark_validated_now(self):
        self.validated_at = datetime.now().isoformat(
            timespec="seconds"
        )