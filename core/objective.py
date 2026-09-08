from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class ExerciseObjective:
    """
    A measurable objective that the exercise is intended to achieve.
    """

    title: str
    description: str = ""

    success_criteria: list[str] = field(default_factory=list)

    supporting_injects: list[int] = field(default_factory=list)
    
    supporting_doctrine: list[str] = field(default_factory=list)

    achieved: bool | None = None
    
@dataclass
class ExerciseObjective:
    """
    A measurable objective that the exercise is intended to achieve.
    """

    title: str
    description: str = ""

    success_criteria: list[str] = field(default_factory=list)

    supporting_injects: list[int] = field(default_factory=list)

    supporting_doctrine: list[str] = field(default_factory=list)

    achieved: bool | None = None

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    def __str__(self):
        return self.title
