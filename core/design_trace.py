from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class DesignTraceEventType(Enum):
    ATTENTION_IDENTIFIED = "Attention Identified"
    PROPOSAL_CREATED = "Proposal Created"
    REVIEW_STARTED = "Review Started"
    DESIGNER_EDITED = "Designer Edited"
    PROPOSAL_ACCEPTED = "Proposal Accepted"
    PROPOSAL_REJECTED = "Proposal Rejected"
    APPLIED_TO_DESIGN = "Applied to Design"


@dataclass
class DesignTraceRecord:
    """
    Records the provenance of a design decision or change.

    A trace record describes what happened, why it happened,
    what informed it and what the resulting design state was.

    It does not itself alter the authoritative exercise design.
    """

    event_type: DesignTraceEventType

    trace_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    objective_title: str = ""
    proposal_id: str = ""

    summary: str = ""
    rationale: str = ""

    original_content: list[str] = field(
        default_factory=list
    )

    proposed_content: list[str] = field(
        default_factory=list
    )

    reviewed_content: list[str] = field(
        default_factory=list
    )

    resulting_content: list[str] = field(
        default_factory=list
    )

    source_references: list[str] = field(
        default_factory=list
    )

    recorded_by: str = ""
    recorded_at: str = ""

    def mark_recorded_now(self):
        self.recorded_at = datetime.now().isoformat(
            timespec="seconds"
        )

    def add_source_reference(
        self,
        reference: str,
    ):
        reference = reference.strip()

        if (
            reference
            and reference not in self.source_references
        ):
            self.source_references.append(
                reference
            )