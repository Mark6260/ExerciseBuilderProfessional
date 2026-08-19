from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class MelMilPromotion:
    """
    Records the controlled promotion of an assured Candidate MEL/MIL
    Activity into the live Project MEL/MIL workspace.

    The workspace currently stores executable MEL/MIL rows as Inject
    objects. This record preserves the design and assurance lineage
    explaining why that Inject exists.
    """

    inject_number: int
    candidate_mel_mil_activity_id: str

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
