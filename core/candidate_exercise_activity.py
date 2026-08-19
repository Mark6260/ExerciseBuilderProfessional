from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class CandidateExerciseActivity:
    """
    A candidate piece of exercise architecture derived from a completed
    Exercise Design Opportunity.

    It is intentionally not an inject. It describes an activity, situation,
    decision point, role-play sequence or other exercise mechanism that could
    create the required opportunity for the training audience.
    """

    title: str
    description: str = ""

    delivery_method: str = ""
    phase: str = ""
    notes: str = ""

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
