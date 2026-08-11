from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class DiscoveryRequirement:
    """
    Describes an unresolved training, evidence or assessment
    requirement for which Exercise Director may search
    authorised planning sources for potential opportunities.

    This object describes what is needed. It does not determine
    whether any discovered activity is suitable.
    """

    requirement_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    title: str = ""
    description: str = ""

    capability_area: str = ""

    required_activities: list[str] = field(
        default_factory=list
    )

    desired_evidence: list[str] = field(
        default_factory=list
    )

    keywords: list[str] = field(
        default_factory=list
    )

    earliest_date: str = ""
    latest_date: str = ""

    related_finding_ids: list[str] = field(
        default_factory=list
    )

    related_recommendation_ids: list[str] = field(
        default_factory=list
    )

    related_action_ids: list[str] = field(
        default_factory=list
    )

    def add_required_activity(self, activity: str):
        if (
            activity
            and activity not in self.required_activities
        ):
            self.required_activities.append(activity)

    def add_desired_evidence(self, evidence: str):
        if (
            evidence
            and evidence not in self.desired_evidence
        ):
            self.desired_evidence.append(evidence)

    def add_keyword(self, keyword: str):
        if keyword and keyword not in self.keywords:
            self.keywords.append(keyword)

    def add_finding_id(self, finding_id: str):
        if (
            finding_id
            and finding_id not in self.related_finding_ids
        ):
            self.related_finding_ids.append(finding_id)

    def add_recommendation_id(
        self,
        recommendation_id: str,
    ):
        if (
            recommendation_id
            and recommendation_id
            not in self.related_recommendation_ids
        ):
            self.related_recommendation_ids.append(
                recommendation_id
            )

    def add_action_id(self, action_id: str):
        if (
            action_id
            and action_id not in self.related_action_ids
        ):
            self.related_action_ids.append(action_id)