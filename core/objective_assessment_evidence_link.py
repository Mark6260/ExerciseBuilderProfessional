from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class ObjectiveAssessmentEvidenceLink:
    criterion_id: str
    activity_id: str
    link_id: str = field(
        default_factory=lambda: str(uuid4())
    )
    