from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class EvidenceType(Enum):
    OBSERVATION = "Observation"
    PERFORMANCE_DATA = "Performance Data"
    ASSESSMENT = "Assessment"
    DOCUMENT = "Document"
    EXERCISE_OUTPUT = "Exercise Output"
    PROFESSIONAL_JUDGEMENT = "Professional Judgement"
    OTHER = "Other"


@dataclass
class EvidenceRecord:
    """
    Records evidence that may support an assessment,
    readiness gap or readiness decision.

    Evidence records what was observed, measured or produced.
    It does not itself determine readiness.
    """

    evidence_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    title: str = ""

    evidence_type: EvidenceType = EvidenceType.OBSERVATION

    description: str = ""

    source: str = ""

    related_standard: str = ""

    related_objective: str = ""

    related_inject: int | None = None

    recorded_by: str = ""

    recorded_at: str = ""

    reference: str = ""

    def mark_recorded_now(self):
        self.recorded_at = datetime.now().isoformat(
            timespec="seconds"
        )