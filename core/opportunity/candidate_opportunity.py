from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4
from core.improvement.training_opportunity import (
    TrainingOpportunity,
    TrainingOpportunityStatus,
)


class OpportunitySourceType(Enum):
    CALENDAR = "Calendar"
    TRAINING_PROGRAMME = "Training Programme"
    EXERCISE_PROGRAMME = "Exercise Programme"
    MEL_MIL = "MEL/MIL"
    PARTNER_ORGANISATION = "Partner Organisation"
    MANUAL = "Manual"
    OTHER = "Other"


class CandidateStatus(Enum):
    DISCOVERED = "Discovered"
    UNDER_REVIEW = "Under Review"
    SUITABLE = "Suitable"
    NOT_SUITABLE = "Not Suitable"
    PROMOTED = "Promoted"


@dataclass
class CandidateOpportunity:
    """
    Records an activity discovered from an authorised planning
    source that may provide a useful training or assessment
    opportunity.

    Discovery does not establish suitability.
    Professional review is required before a candidate becomes
    a validated TrainingOpportunity.
    """

    candidate_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    title: str = ""
    organisation: str = ""
    description: str = ""

    start_date: str = ""
    end_date: str = ""
    location: str = ""

    source_type: OpportunitySourceType = (
        OpportunitySourceType.OTHER
    )

    source_name: str = ""
    source_reference: str = ""

    status: CandidateStatus = CandidateStatus.DISCOVERED

    related_finding_ids: list[str] = field(
        default_factory=list
    )

    related_recommendation_ids: list[str] = field(
        default_factory=list
    )

    related_action_ids: list[str] = field(
        default_factory=list
    )

    relevance_reasons: list[str] = field(
        default_factory=list
    )

    review_reason: str = ""
    review_notes: str = ""
    reviewed_by: str = ""
    reviewed_at: str = ""

    identified_at: str = ""

    promoted_opportunity_id: str = ""

    def add_finding_id(self, finding_id: str):
        if (
            finding_id
            and finding_id not in self.related_finding_ids
        ):
            self.related_finding_ids.append(finding_id)

    def add_recommendation_id(self, recommendation_id: str):
        if (
            recommendation_id
            and recommendation_id
            not in self.related_recommendation_ids
        ):
            self.related_recommendation_ids.append(
                recommendation_id
            )

    def add_action_id(self, action_id: str):
        if (
            action_id
            and action_id not in self.related_action_ids
        ):
            self.related_action_ids.append(action_id)

    def add_relevance_reason(self, reason: str):
        if reason and reason not in self.relevance_reasons:
            self.relevance_reasons.append(reason)

    def mark_identified_now(self):
        self.identified_at = datetime.now().isoformat(
            timespec="seconds"
        )

    def mark_reviewed_now(self):
        self.reviewed_at = datetime.now().isoformat(
            timespec="seconds"
        )

    def mark_under_review(
        self,
        reviewed_by: str,
        notes: str = "",
    ):
        self.status = CandidateStatus.UNDER_REVIEW
        self.reviewed_by = reviewed_by
        self.review_notes = notes
        self.review_reason = ""
        self.mark_reviewed_now()

    def mark_suitable(
        self,
        reviewed_by: str,
        reason: str,
        notes: str = "",
    ):
        if not reason.strip():
            raise ValueError(
                "A reason is required when marking "
                "a candidate opportunity as suitable."
            )

        self.status = CandidateStatus.SUITABLE
        self.reviewed_by = reviewed_by
        self.review_reason = reason.strip()
        self.review_notes = notes
        self.mark_reviewed_now()

    def mark_not_suitable(
        self,
        reviewed_by: str,
        reason: str,
        notes: str = "",
    ):
        if not reason.strip():
            raise ValueError(
                "A reason is required when marking "
                "a candidate opportunity as not suitable."
            )

        self.status = CandidateStatus.NOT_SUITABLE
        self.reviewed_by = reviewed_by
        self.review_reason = reason.strip()
        self.review_notes = notes
        self.mark_reviewed_now()

    def promote_to_training_opportunity(
        self,
        promoted_by: str,
    ) -> TrainingOpportunity:
        if self.status != CandidateStatus.SUITABLE:
            raise ValueError(
                "Only a suitable candidate opportunity "
                "can be promoted."
            )

        if not promoted_by.strip():
            raise ValueError(
                "The person promoting the candidate "
                "must be recorded."
            )

        opportunity = TrainingOpportunity(
            title=self.title,
            organisation=self.organisation,
            description=self.description,
            start_date=self.start_date,
            end_date=self.end_date,
            location=self.location,
            status=TrainingOpportunityStatus.POTENTIAL,
            related_finding_ids=list(
                self.related_finding_ids
            ),
            related_recommendation_ids=list(
                self.related_recommendation_ids
            ),
            related_action_ids=list(
                self.related_action_ids
            ),
            suitability_rationale=self.review_reason,
            access_confirmed=False,
            assessment_arrangements_confirmed=False,
            identified_by=promoted_by.strip(),
        )

        opportunity.mark_identified_now()

        self.promoted_opportunity_id = (
            opportunity.opportunity_id
        )
        self.status = CandidateStatus.PROMOTED

        return opportunity