from dataclasses import dataclass, field


@dataclass
class ExerciseObjective:
    """
    A measurable objective that the exercise is intended to achieve.
    """

    title: str
    description: str = ""

    success_criteria: list[str] = field(default_factory=list)

    supporting_injects: list[int] = field(default_factory=list)

    achieved: bool | None = None