from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class ReadinessDecisionOutcome(Enum):
    NOT_ASSESSED = "Not Assessed"
    READY = "Ready"
    READY_WITH_LIMITATIONS = "Ready With Limitations"
    NOT_YET_READY = "Not Yet Ready"
    UNABLE_TO_ASSESS = "Unable To Assess"


class AssessmentExceptionReason(Enum):
    ENVIRONMENTAL_CONSTRAINT = "Environmental Constraint"
    SAFETY_CONSTRAINT = "Safety Constraint"
    EXERCISE_DIRECTION = "Exercise Direction"
    OPERATIONAL_PRIORITY = "Operational Priority"
    RESOURCE_CONSTRAINT = "Resource Constraint"
    TECHNICAL_FAILURE = "Technical Failure"
    TIME_CONSTRAINT = "Time Constraint"
    REAL_WORLD_EVENT = "Real World Event"
    OTHER = "Other"

@dataclass
class ReadinessDecision:
    """
    Records an authorised professional judgement about readiness.

    The decision is made by a person, not by Exercise Director.
    Exercise Director preserves the decision, its rationale,
    the assessments considered and any limitations or exceptions.
    """

    decision_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    outcome: ReadinessDecisionOutcome = (
        ReadinessDecisionOutcome.NOT_ASSESSED
    )

    assessment_ids: list[str] = field(
        default_factory=list
    )

    rationale: str = ""
    limitations: str = ""
    required_action: str = ""

    decision_maker: str = ""
    decision_authority: str = ""
    recorded_at: str = ""

    exception_reason: AssessmentExceptionReason | None = None
    exception_explanation: str = ""

    def add_assessment_id(self, assessment_id: str):
        if (
            assessment_id
            and assessment_id not in self.assessment_ids
        ):
            self.assessment_ids.append(assessment_id)

    def mark_recorded_now(self):
        self.recorded_at = datetime.now().isoformat(
            timespec="seconds"
        )