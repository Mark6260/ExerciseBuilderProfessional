from dataclasses import dataclass, field


@dataclass
class Capability:
    """
    Describes the operational capability that an exercise
    is intended to develop.
    """

    title: str
    description: str = ""

    collective_training_objectives: list[str] = field(
        default_factory=list
    )