from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class AssessmentOutcome(Enum):
    NOT_ASSESSED = "Not Assessed"
    ACHIEVED = "Achieved"
    PARTIALLY_ACHIEVED = "Partially Achieved"
    NOT_ACHIEVED = "Not Achieved"


@dataclass
class AssessmentRecord:
    """
    Records an instructor's assessment of performance against
    an exercise objective during an inject.

    The assessment preserves the professional judgement and
    identifies the evidence considered when reaching it.
    """

    inject_number: int
    objective_title: str

    assessment_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    outcome: AssessmentOutcome = AssessmentOutcome.NOT_ASSESSED

    evidence_ids: list[str] = field(
        default_factory=list
    )

    comments: str = ""

    assessor: str = ""

    recorded_at: str = ""

    def add_evidence_id(self, evidence_id: str):
        if evidence_id and evidence_id not in self.evidence_ids:
            self.evidence_ids.append(evidence_id)

    def mark_recorded_now(self):
        self.recorded_at = datetime.now().isoformat(
            timespec="seconds"
        )