from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from .scope import PreparednessScope
from uuid import uuid4





class ConfidenceStage(Enum):
    PRE_EXERCISE = "Pre Exercise"
    POST_EXERCISE = "Post Exercise"

ConfidenceScope = PreparednessScope


@dataclass
class ConfidenceAssessment:
    """
    Records self-reported confidence at a point in the
    training journey.

    Confidence belongs to the trainee or training audience.
    It records perception and does not itself demonstrate
    capability, readiness or proficiency.
    """

    assessment_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    exercise_id: str = ""

    scope: PreparednessScope = PreparednessScope.INDIVIDUAL
    subject_id: str = ""

    related_objective_ids: list[str] = field(
        default_factory=list
    )

    stage: ConfidenceStage = ConfidenceStage.PRE_EXERCISE
    ConfidenceScope = PreparednessScope

    # None means Not Assessed.
    # A recorded assessment must use the 1–5 confidence scale.
    confidence_score: int | None = None

    reflection: str = ""

    recorded_at: str = ""

    def add_objective_id(self, objective_id: str):
        if (
            objective_id
            and objective_id not in self.related_objective_ids
        ):
            self.related_objective_ids.append(
                objective_id
            )

    def set_confidence_score(self, score: int | None):
        if score is not None and not 1 <= score <= 5:
            raise ValueError(
                "Confidence score must be between 1 and 5, "
                "or None for Not Assessed."
            )

        self.confidence_score = score

    def mark_recorded_now(self):
        self.recorded_at = datetime.now().isoformat(
            timespec="seconds"
        )