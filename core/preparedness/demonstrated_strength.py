from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from .scope import PreparednessScope


@dataclass
class DemonstratedStrength:
    """
    Records a positive, evidence-backed strength demonstrated
    during training.

    A demonstrated strength may support zero, one or several
    exercise objectives.

    It cannot exist as a professional claim without supporting
    evidence.
    """

    strength_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    exercise_id: str = ""

    scope: PreparednessScope = PreparednessScope.INDIVIDUAL
    subject_id: str = ""

    title: str = ""
    description: str = ""

    related_objective_ids: list[str] = field(
        default_factory=list
    )

    related_evidence_ids: list[str] = field(
        default_factory=list
    )

    identified_by: str = ""
    recorded_at: str = ""

    def add_objective_id(self, objective_id: str):
        if (
            objective_id
            and objective_id not in self.related_objective_ids
        ):
            self.related_objective_ids.append(
                objective_id
            )

    def add_evidence_id(self, evidence_id: str):
        if (
            evidence_id
            and evidence_id not in self.related_evidence_ids
        ):
            self.related_evidence_ids.append(
                evidence_id
            )

    def validate(self):
        if not self.related_evidence_ids:
            raise ValueError(
                "A demonstrated strength must be supported "
                "by evidence."
            )

    def mark_recorded_now(self):
        self.recorded_at = datetime.now().isoformat(
            timespec="seconds"
        )