from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class PlanningSourceType(Enum):
    CALENDAR = "Calendar"
    TRAINING_PROGRAMME = "Training Programme"
    EXERCISE_PROGRAMME = "Exercise Programme"
    MEL_MIL = "MEL/MIL"
    PARTNER_ORGANISATION = "Partner Organisation"
    MANUAL = "Manual"
    OTHER = "Other"


class PlanningSourceStatus(Enum):
    PROPOSED = "Proposed"
    AUTHORISED = "Authorised"
    SUSPENDED = "Suspended"
    WITHDRAWN = "Withdrawn"


@dataclass
class PlanningSource:
    """
    Records a planning source that may provide activities for
    opportunity discovery.

    A source must be explicitly authorised before Exercise
    Director may use it for automated candidate discovery.
    """

    source_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    name: str = ""
    organisation: str = ""
    source_type: PlanningSourceType = PlanningSourceType.OTHER

    description: str = ""
    reference: str = ""

    status: PlanningSourceStatus = PlanningSourceStatus.PROPOSED

    authorised_for_discovery: bool = False

    authorised_by: str = ""
    authority: str = ""
    authorised_at: str = ""

    authorisation_notes: str = ""

    suspended_by: str = ""
    suspended_at: str = ""
    suspension_reason: str = ""

    withdrawn_by: str = ""
    withdrawn_at: str = ""
    withdrawal_reason: str = ""

    def authorise(
        self,
        authorised_by: str,
        authority: str,
        notes: str = "",
    ):
        if not authorised_by.strip():
            raise ValueError(
                "The person authorising the planning source "
                "must be recorded."
            )

        if not authority.strip():
            raise ValueError(
                "The authority for use of the planning source "
                "must be recorded."
            )

        self.status = PlanningSourceStatus.AUTHORISED
        self.authorised_for_discovery = True
        self.authorised_by = authorised_by.strip()
        self.authority = authority.strip()
        self.authorisation_notes = notes
        self.authorised_at = datetime.now().isoformat(
            timespec="seconds"
        )

    def suspend(
        self,
        suspended_by: str,
        reason: str,
    ):
        if not suspended_by.strip():
            raise ValueError(
                "The person suspending the planning source "
                "must be recorded."
            )

        if not reason.strip():
            raise ValueError(
                "A reason is required when suspending "
                "a planning source."
            )

        self.status = PlanningSourceStatus.SUSPENDED
        self.authorised_for_discovery = False
        self.suspended_by = suspended_by.strip()
        self.suspension_reason = reason.strip()
        self.suspended_at = datetime.now().isoformat(
            timespec="seconds"
        )

    def withdraw(
        self,
        withdrawn_by: str,
        reason: str,
    ):
        if not withdrawn_by.strip():
            raise ValueError(
                "The person withdrawing the planning source "
                "must be recorded."
            )

        if not reason.strip():
            raise ValueError(
                "A reason is required when withdrawing "
                "a planning source."
            )

        self.status = PlanningSourceStatus.WITHDRAWN
        self.authorised_for_discovery = False
        self.withdrawn_by = withdrawn_by.strip()
        self.withdrawal_reason = reason.strip()
        self.withdrawn_at = datetime.now().isoformat(
            timespec="seconds"
        )

    def can_be_used_for_discovery(self) -> bool:
        return (
            self.status == PlanningSourceStatus.AUTHORISED
            and self.authorised_for_discovery
        )