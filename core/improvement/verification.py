from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class VerificationOutcome(Enum):
    RESOLVED = "Resolved"
    PARTIALLY_RESOLVED = "Partially Resolved"
    NOT_RESOLVED = "Not Resolved"
    INSUFFICIENT_EVIDENCE = "Insufficient Evidence"


class VerificationFollowUpState(Enum):
    CLOSED = "Closed"
    FURTHER_IMPROVEMENT_REQUIRED = "Further Improvement Required"
    FURTHER_EVIDENCE_REQUIRED = "Further Evidence Required"


@dataclass
class ImprovementVerification:
    """
    Records a professional assessment of whether the underlying issue
    associated with a completed improvement action has been resolved.

    Verification is separate from action completion.

    A completed action records that an authorised task was carried out.
    A verification records the assessor's judgement, based on available
    evidence, about whether the underlying issue has actually been
    resolved.

    This record does not alter the original finding, recommendation or
    improvement action.
    """

    verification_id: str = field(default_factory=lambda: str(uuid4()))
    related_action_id: str = ""
    related_finding_ids: list[str] = field(default_factory=list)
    related_evidence_ids: list[str] = field(default_factory=list)

    outcome: VerificationOutcome = VerificationOutcome.INSUFFICIENT_EVIDENCE
    rationale: str = ""

    assessed_by: str = ""
    assessment_authority: str = ""
    recorded_at: str = ""

    def add_finding_id(self, finding_id: str):
        if finding_id and finding_id not in self.related_finding_ids:
            self.related_finding_ids.append(finding_id)

    def add_evidence_id(self, evidence_id: str):
        if evidence_id and evidence_id not in self.related_evidence_ids:
            self.related_evidence_ids.append(evidence_id)

    def mark_recorded_now(self):
        self.recorded_at = datetime.now().isoformat(timespec="seconds")

    def follow_up_state(self) -> VerificationFollowUpState:
        """
        Derive the permitted follow-up state from the immutable
        verification outcome.

        This method does not create a recommendation, action, evidence
        record or assessment. It only reports what kind of follow-up is
        required by the recorded verification outcome.
        """

        if self.outcome == VerificationOutcome.RESOLVED:
            return VerificationFollowUpState.CLOSED

        if self.outcome in {
            VerificationOutcome.PARTIALLY_RESOLVED,
            VerificationOutcome.NOT_RESOLVED,
        }:
            return VerificationFollowUpState.FURTHER_IMPROVEMENT_REQUIRED

        return VerificationFollowUpState.FURTHER_EVIDENCE_REQUIRED

    def requires_follow_up(self) -> bool:
        return self.follow_up_state() != VerificationFollowUpState.CLOSED
