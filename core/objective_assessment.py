from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4

from core.objective_assessment_evidence_link import (
    ObjectiveAssessmentEvidenceLink,
)


class ObjectiveAssessmentJudgement(Enum):
    INSUFFICIENT_EVIDENCE = "Insufficient Evidence"
    PARTIALLY_DEMONSTRATED = "Partially Demonstrated"
    DEMONSTRATED = "Demonstrated"


@dataclass
class ObjectiveAssessment:
    objective_id: str
    delivery_session_id: str
    judgement: ObjectiveAssessmentJudgement

    assessment_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    evidence_links: list[
        ObjectiveAssessmentEvidenceLink
    ] = field(
        default_factory=list
    )

    rationale: str = ""
    limitations: str = ""
    assessed_by: str = ""
    assessed_at: str = ""