from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AssessmentOutcome(Enum):
    NOT_ASSESSED = "Not Assessed"
    ACHIEVED = "Achieved"
    PARTIALLY_ACHIEVED = "Partially Achieved"
    NOT_ACHIEVED = "Not Achieved"


@dataclass
class AssessmentRecord:
    """
    Records an instructor's assessment of performance against
    an exercise objective during an inject.
    """

    inject_number: int
    objective_title: str

    outcome: AssessmentOutcome = AssessmentOutcome.NOT_ASSESSED
    comments: str = ""
    assessor: str = ""
    recorded_at: str = ""

    def mark_recorded_now(self):
        self.recorded_at = datetime.now().isoformat(
            timespec="seconds"
        )