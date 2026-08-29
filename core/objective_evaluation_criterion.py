from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class ObjectiveEvaluationCriterion:
    objective_id: str
    description: str
    observable_evidence: str
    criterion_id: str = field(
        default_factory=lambda: str(uuid4())
    )
    