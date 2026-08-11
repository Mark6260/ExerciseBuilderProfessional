from core.opportunity.candidate_opportunity import (
    CandidateOpportunity,
    OpportunitySourceType,
)
from core.opportunity.discovery_requirement import (
    DiscoveryRequirement,
)
from core.opportunity.planned_activity import (
    PlannedActivity,
    PlannedActivitySourceType,
)
from datetime import date
from core.opportunity.planning_source import PlanningSource


class OpportunityDiscoveryEngine:
    """
    Compares unresolved discovery requirements with planned
    activities from authorised sources.

    The engine may surface a CandidateOpportunity and explain
    why it appears relevant.

    It does not determine professional suitability.
    """

    def discover_from_authorised_source(
        self,
        requirement: DiscoveryRequirement,
        activity: PlannedActivity,
        source: PlanningSource,
    ) -> CandidateOpportunity | None:
        if not source.can_be_used_for_discovery():
            raise PermissionError(
                "Planning source is not authorised "
                "for opportunity discovery."
            )

        candidate = self.discover_candidate(
            requirement,
            activity,
        )

        if candidate is None:
            return None

        candidate.source_name = source.name
        candidate.source_reference = source.reference

        candidate.add_relevance_reason(
            "Activity obtained from an authorised "
            "planning source."
        )

        return candidate

    def discover_candidate(
        self,
        requirement: DiscoveryRequirement,
        activity: PlannedActivity,
    ) -> CandidateOpportunity | None:
        reasons = []

        if not self._activity_within_date_window(
            requirement,
            activity,
        ):
            return None
        if (
            requirement.earliest_date
            or requirement.latest_date
        ):
            reasons.append(
                "Activity falls within required "
                "reassessment window."
        )

        requirement_text = " ".join(
            [
                requirement.title,
                requirement.description,
                requirement.capability_area,
                *requirement.required_activities,
                *requirement.desired_evidence,
                *requirement.keywords,
            ]
        ).lower()

        activity_text = " ".join(
            [
                activity.title,
                activity.description,
                *activity.activity_tags,
                *activity.capability_tags,
            ]
        ).lower()

        if (
            requirement.capability_area
            and requirement.capability_area.lower()
            in activity_text
        ):
            reasons.append(
                "Capability area appears relevant."
            )

        for required_activity in requirement.required_activities:
            if (
                required_activity
                and required_activity.lower() in activity_text
            ):
                reasons.append(
                    f"Relevant activity identified: "
                    f"{required_activity}"
                )

        for keyword in requirement.keywords:
            if keyword and keyword.lower() in activity_text:
                reasons.append(
                    f"Relevant keyword identified: {keyword}"
                )

        for capability_tag in activity.capability_tags:
            if (
                capability_tag
                and capability_tag.lower() in requirement_text
            ):
                reasons.append(
                    f"Relevant capability tag identified: "
                    f"{capability_tag}"
                )

        if not reasons:
            return None

        candidate = CandidateOpportunity(
            title=activity.title,
            organisation=activity.organisation,
            description=activity.description,
            start_date=activity.start_date,
            end_date=activity.end_date,
            location=activity.location,
            source_type=self._map_source_type(
                activity.source_type
            ),
            source_name=activity.source_name,
            source_reference=activity.source_reference,
        )

        for finding_id in requirement.related_finding_ids:
            candidate.add_finding_id(finding_id)

        for recommendation_id in (
            requirement.related_recommendation_ids
        ):
            candidate.add_recommendation_id(
                recommendation_id
            )

        for action_id in requirement.related_action_ids:
            candidate.add_action_id(action_id)

        for reason in reasons:
            candidate.add_relevance_reason(reason)

        candidate.mark_identified_now()

        return candidate

    @staticmethod
    def _activity_within_date_window(
        requirement: DiscoveryRequirement,
        activity: PlannedActivity,
    ) -> bool:
        if not (
            requirement.earliest_date
            or requirement.latest_date
        ):
            return True

        if not activity.start_date:
            return True

        try:
            activity_start = date.fromisoformat(
                activity.start_date
            )

            activity_end = date.fromisoformat(
                activity.end_date
                or activity.start_date
            )

            earliest = (
                date.fromisoformat(requirement.earliest_date)
                if requirement.earliest_date
                else None
            )

            latest = (
                date.fromisoformat(requirement.latest_date)
                if requirement.latest_date
                else None
            )
        except ValueError:
            return True

        if earliest and activity_end < earliest:
            return False

        if latest and activity_start > latest:
            return False

        return True

    @staticmethod
    def _map_source_type(
        source_type: PlannedActivitySourceType,
    ) -> OpportunitySourceType:
        mapping = {
            PlannedActivitySourceType.CALENDAR:
                OpportunitySourceType.CALENDAR,

            PlannedActivitySourceType.TRAINING_PROGRAMME:
                OpportunitySourceType.TRAINING_PROGRAMME,

            PlannedActivitySourceType.EXERCISE_PROGRAMME:
                OpportunitySourceType.EXERCISE_PROGRAMME,

            PlannedActivitySourceType.MEL_MIL:
                OpportunitySourceType.MEL_MIL,

            PlannedActivitySourceType.PARTNER_ORGANISATION:
                OpportunitySourceType.PARTNER_ORGANISATION,

            PlannedActivitySourceType.MANUAL:
                OpportunitySourceType.MANUAL,

            PlannedActivitySourceType.OTHER:
                OpportunitySourceType.OTHER,
        }

        return mapping.get(
            source_type,
            OpportunitySourceType.OTHER,
        )
