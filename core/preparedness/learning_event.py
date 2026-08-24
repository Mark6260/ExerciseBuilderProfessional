from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4
from .scope import PreparednessScope


class LearningOpportunityState(Enum):
    RECEIVED = "Received"
    EXPLOITED = "Exploited"
    SUBSEQUENTLY_DEMONSTRATED = "Subsequently Demonstrated"


@dataclass
class LearningEvent:
    """
    Records a learning opportunity encountered during training.

    A learning event may be planned or emergent.

    Received records that the opportunity occurred.
    Exploited records that the trainee or team acted on the opportunity.
    Subsequently Demonstrated records that later evidence supports
    a claim that the learning was demonstrated in subsequent performance.

    A LearningEvent is not itself evidence.
    """

    learning_event_id: str = field(
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

    state: LearningOpportunityState = (
        LearningOpportunityState.RECEIVED
    )

    related_evidence_ids: list[str] = field(
        default_factory=list
    )

    subsequent_evidence_ids: list[str] = field(
        default_factory=list
    )

    reflection: str = ""

    recorded_by: str = ""
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

    def add_subsequent_evidence_id(self, evidence_id: str):
        if (
            evidence_id
            and evidence_id not in self.subsequent_evidence_ids
        ):
            self.subsequent_evidence_ids.append(
                evidence_id
            )

    def set_state(self, state: LearningOpportunityState):
        if (
            state == LearningOpportunityState.EXPLOITED
            and not self.related_evidence_ids
        ):
            raise ValueError(
                "An exploited learning opportunity must be "
                "supported by evidence."
            )

        if (
            state
            == LearningOpportunityState.SUBSEQUENTLY_DEMONSTRATED
            and not self.subsequent_evidence_ids
        ):
            raise ValueError(
                "Subsequently demonstrated learning must be "
                "supported by later evidence."
            )

        self.state = state

    def mark_recorded_now(self):
        self.recorded_at = datetime.now().isoformat(
            timespec="seconds"
        )