from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class RecommendationType(Enum):
    CORRECTIVE = "Corrective"
    IMPROVEMENT = "Improvement"
    SUSTAINMENT = "Sustainment"
    FURTHER_ASSESSMENT = "Further Assessment"
    TRAINING_OPPORTUNITY = "Training Opportunity"
    OTHER = "Other"


class RecommendationDisposition(Enum):
    NOT_REVIEWED = "Not Reviewed"
    ACCEPTED = "Accepted"
    ACCEPTED_IN_PART = "Accepted In Part"
    DEFERRED = "Deferred"
    NOT_ACCEPTED = "Not Accepted"


@dataclass
class Recommendation:
    """
    Records professional advice arising from a finding.

    A recommendation identifies something that may assist.
    It does not itself create or authorise an action.
    """

    recommendation_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    title: str = ""

    recommendation_type: RecommendationType = (
        RecommendationType.IMPROVEMENT
    )

    description: str = ""

    related_finding_ids: list[str] = field(
        default_factory=list
    )

    disposition: RecommendationDisposition = (
        RecommendationDisposition.NOT_REVIEWED
    )

    disposition_rationale: str = ""
    disposition_by: str = ""
    disposition_authority: str = ""
    disposition_at: str = ""

    recommended_by: str = ""
    recorded_at: str = ""

    def add_finding_id(self, finding_id: str):
        if (
            finding_id
            and finding_id not in self.related_finding_ids
        ):
            self.related_finding_ids.append(finding_id)

    def mark_recorded_now(self):
        self.recorded_at = datetime.now().isoformat(
            timespec="seconds"
        )

    def mark_dispositioned_now(self):
        self.disposition_at = datetime.now().isoformat(
            timespec="seconds"
        )