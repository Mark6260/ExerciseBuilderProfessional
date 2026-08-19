from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class ExerciseDesignOpportunity:
    """
    A designer-authored opportunity for the training audience to
    demonstrate assured collective performance during the exercise.

    It sits between the assured CTO and later MEL/MIL or inject design.
    The opportunity describes what the exercise must make possible;
    it does not prescribe a specific inject.
    """

    title: str
    description: str = ""

    # Brick 8: designer-authored decomposition of the opportunity.
    # These fields describe what later MEL/MIL activity must enable;
    # they are not inject text.
    required_conditions: str = ""
    stimulus_information: str = ""
    response_opportunity: str = ""
    evidence_capture_plan: str = ""

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
