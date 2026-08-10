from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class FindingType(Enum):
    STRENGTH = "Strength"
    IMPROVEMENT = "Improvement"
    EVIDENCE_GAP = "Evidence Gap"
    READINESS_GAP = "Readiness Gap"
    OBSERVATION = "Observation"
    OTHER = "Other"


@dataclass
class Finding:
    """
    Records something learned or identified through an exercise,
    assessment or readiness decision.

    A finding records what was identified.
    It does not itself prescribe an action.
    """

    finding_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    title: str = ""

    finding_type: FindingType = FindingType.OBSERVATION

    description: str = ""

    related_decision_id: str = ""
    related_assessment_ids: list[str] = field(
        default_factory=list
    )
    related_evidence_ids: list[str] = field(
        default_factory=list
    )

    recorded_by: str = ""
    recorded_at: str = ""

    def add_assessment_id(self, assessment_id: str):
        if (
            assessment_id
            and assessment_id not in self.related_assessment_ids
        ):
            self.related_assessment_ids.append(assessment_id)

    def add_evidence_id(self, evidence_id: str):
        if (
            evidence_id
            and evidence_id not in self.related_evidence_ids
        ):
            self.related_evidence_ids.append(evidence_id)

    def mark_recorded_now(self):
        self.recorded_at = datetime.now().isoformat(
            timespec="seconds"
        )