from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4
from core.evidence import EvidenceRecord, EvidenceType


class ObservationType(Enum):
    EFFECTIVE_PRACTICE = "Effective Practice"
    OBSERVATION = "Observation"
    CONCERN = "Concern"
    EVIDENCE_GAP = "Evidence Gap"


class ObservationStatus(Enum):
    DRAFT = "Draft"
    RECORDED = "Recorded"
    REVIEWED = "Reviewed"
    WITHDRAWN = "Withdrawn"


@dataclass
class Observation:
    """
    Records what an authorised observer saw, heard, or otherwise
    directly observed during exercise or training activity.

    An Observation records evidence. It does not determine an
    assessment outcome or readiness decision.
    """

    observation_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    exercise_time: str = ""
    observed_at: str = ""

    observer_name: str = ""
    observer_role: str = ""

    observation_type: ObservationType = (
        ObservationType.OBSERVATION
    )

    title: str = ""
    description: str = ""

    related_inject_number: int | None = None
    related_objective_titles: list[str] = field(
        default_factory=list
    )
    related_activity_id: str = ""

    evidence_ids: list[str] = field(
        default_factory=list
    )

    status: ObservationStatus = ObservationStatus.DRAFT

    recorded_at: str = ""
    reviewed_by: str = ""
    reviewed_at: str = ""

    withdrawal_reason: str = ""
    withdrawn_by: str = ""
    withdrawn_at: str = ""

    def add_objective(self, objective_title: str):
        objective_title = objective_title.strip()

        if (
            objective_title
            and objective_title
            not in self.related_objective_titles
        ):
            self.related_objective_titles.append(
                objective_title
            )

    def add_evidence_id(self, evidence_id: str):
        evidence_id = evidence_id.strip()

        if (
            evidence_id
            and evidence_id not in self.evidence_ids
        ):
            self.evidence_ids.append(evidence_id)

    def record(
        self,
        observer_name: str,
        observer_role: str = "",
    ):
        if not observer_name.strip():
            raise ValueError(
                "The observer must be recorded."
            )

        if not self.description.strip():
            raise ValueError(
                "An observation must describe what was observed."
            )

        self.observer_name = observer_name.strip()
        self.observer_role = observer_role.strip()

        if not self.observed_at:
            self.observed_at = datetime.now().isoformat(
                timespec="seconds"
            )

        self.recorded_at = datetime.now().isoformat(
            timespec="seconds"
        )

        self.status = ObservationStatus.RECORDED

    def mark_reviewed(
        self,
        reviewed_by: str,
    ):
        if not reviewed_by.strip():
            raise ValueError(
                "The reviewer must be recorded."
            )

        if self.status != ObservationStatus.RECORDED:
            raise ValueError(
                "Only a recorded observation can be reviewed."
            )

        self.reviewed_by = reviewed_by.strip()
        self.reviewed_at = datetime.now().isoformat(
            timespec="seconds"
        )
        self.status = ObservationStatus.REVIEWED

    def to_evidence_record(self) -> EvidenceRecord:
        if self.status != ObservationStatus.REVIEWED:
            raise ValueError(
                "Only a reviewed observation can be converted "
                "to an evidence record."
            )

        source_parts = [
            self.observer_name,
            self.observer_role,
        ]

        source = " - ".join(
            part for part in source_parts if part
        )

        related_objective = (
            self.related_objective_titles[0]
            if self.related_objective_titles
            else ""
        )

        evidence = EvidenceRecord(
            title=self.title,
            evidence_type=EvidenceType.OBSERVATION,
            description=self.description,
            source=source,
            related_objective=related_objective,
            related_inject=self.related_inject_number,
            recorded_by=self.observer_name,
            recorded_at=self.recorded_at,
            reference=self.observation_id,
        )

        self.add_evidence_id(
            evidence.evidence_id
        )

        return evidence

    def withdraw(
        self,
        withdrawn_by: str,
        reason: str,
    ):
        if not withdrawn_by.strip():
            raise ValueError(
                "The person withdrawing the observation "
                "must be recorded."
            )

        if not reason.strip():
            raise ValueError(
                "A reason is required when withdrawing "
                "an observation."
            )

        self.withdrawn_by = withdrawn_by.strip()
        self.withdrawal_reason = reason.strip()
        self.withdrawn_at = datetime.now().isoformat(
            timespec="seconds"
        )
        self.status = ObservationStatus.WITHDRAWN
