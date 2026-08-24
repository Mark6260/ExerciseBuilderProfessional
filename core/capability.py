from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Capability:
    """
    Describes an operational capability that training
    or exercising is intended to develop or demonstrate.

    A Capability provides a stable reference across training
    events. Exercise-specific objectives may relate to the same
    capability without altering the historical record of either
    exercise.
    """

    title: str
    description: str = ""

    capability_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    collective_training_objectives: list[str] = field(
        default_factory=list
    )

    related_exercise_objectives: list[str] = field(
        default_factory=list
    )

    def add_collective_training_objective(
        self,
        objective_id: str,
    ):
        if (
            objective_id
            and objective_id
            not in self.collective_training_objectives
        ):
            self.collective_training_objectives.append(
                objective_id
            )

    def add_exercise_objective(
        self,
        objective_id: str,
    ):
        if (
            objective_id
            and objective_id
            not in self.related_exercise_objectives
        ):
            self.related_exercise_objectives.append(
                objective_id
            )