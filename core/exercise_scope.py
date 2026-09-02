from dataclasses import dataclass, field


@dataclass
class ExerciseScope:
    """
    Defines the agreed scope for an exercise before
    detailed exercise design begins.
    """

    purpose: str = ""
    aim: str = ""

    in_scope: list[str] = field(
        default_factory=list
    )
    out_of_scope: list[str] = field(
        default_factory=list
    )

    constraints: list[str] = field(
        default_factory=list
    )
    assumptions: list[str] = field(
        default_factory=list
    )

    exercise_type: str = ""
    proposed_approach: str = ""
    scenario_proposition: str = ""
    intended_end_state: str = ""