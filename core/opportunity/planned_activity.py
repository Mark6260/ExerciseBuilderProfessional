from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class PlannedActivitySourceType(Enum):
    CALENDAR = "Calendar"
    TRAINING_PROGRAMME = "Training Programme"
    EXERCISE_PROGRAMME = "Exercise Programme"
    MEL_MIL = "MEL/MIL"
    PARTNER_ORGANISATION = "Partner Organisation"
    MANUAL = "Manual"
    OTHER = "Other"


@dataclass
class PlannedActivity:
    """
    Represents an activity obtained from an authorised planning source.

    A PlannedActivity records what the source says is planned.
    It does not itself imply relevance, suitability or availability
    as a training opportunity.
    """

    activity_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    title: str = ""
    organisation: str = ""
    description: str = ""

    start_date: str = ""
    end_date: str = ""
    location: str = ""

    source_type: PlannedActivitySourceType = (
        PlannedActivitySourceType.OTHER
    )

    source_name: str = ""
    source_reference: str = ""

    activity_tags: list[str] = field(
        default_factory=list
    )

    capability_tags: list[str] = field(
        default_factory=list
    )

    participants: list[str] = field(
        default_factory=list
    )

    def add_activity_tag(self, tag: str):
        if tag and tag not in self.activity_tags:
            self.activity_tags.append(tag)

    def add_capability_tag(self, tag: str):
        if tag and tag not in self.capability_tags:
            self.capability_tags.append(tag)

    def add_participant(self, participant: str):
        if (
            participant
            and participant not in self.participants
        ):
            self.participants.append(participant)