from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class CandidateMelMilActivity:
    """
    A candidate MEL/MIL-level activity derived from a Candidate Exercise
    Activity.

    It is still a design object, not a final inject. It describes an
    executable event or control activity that could later be promoted into
    the MEL/MIL while preserving the assurance lineage that justifies it.
    """

    title: str
    activity_type: str = ""
    phase: str = ""
    timing_window: str = ""

    event_summary: str = ""
    intended_effect: str = ""
    control_notes: str = ""

    candidate_activity_id: str = ""
    design_opportunity_id: str = ""
    cto_id: str = ""
    collective_task_id: str = ""
    success_factor_id: str = ""

    metric_ids: list[str] = field(
        default_factory=list
    )
    evidence_requirement_ids: list[str] = field(
        default_factory=list
    )

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    def __str__(self):
        return self.title
