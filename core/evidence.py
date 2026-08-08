from dataclasses import dataclass
from datetime import datetime
from enum import Enum


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