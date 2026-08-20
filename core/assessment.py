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
    Records a professional assessment of exercise performance.

    An assessment may relate to a legacy Exercise Objective or to the
    assured CTO lineage carried through Exercise Design and MEL/MIL.

    Exercise Director preserves the judgement and the evidence considered.
    It does not make the professional judgement itself.
    """

    inject_number: int = 0
    objective_title: str = ""

    assessment_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    cto_id: str = ""
    collective_task_id: str = ""
    success_factor_id: str = ""

    metric_ids: list[str] = field(
        default_factory=list
    )

    evidence_requirement_ids: list[str] = field(
        default_factory=list
    )

    outcome: AssessmentOutcome = (
        AssessmentOutcome.NOT_ASSESSED
    )

    evidence_ids: list[str] = field(
        default_factory=list
    )

    comments: str = ""
    assessor: str = ""
    recorded_at: str = ""

    def add_evidence_id(self, evidence_id: str):
        if (
            evidence_id
            and evidence_id not in self.evidence_ids
        ):
            self.evidence_ids.append(
                evidence_id
            )

    def mark_recorded_now(self):
        self.recorded_at = datetime.now().isoformat(
            timespec="seconds"
        )