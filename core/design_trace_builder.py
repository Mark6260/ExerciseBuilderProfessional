from core.design_trace import (
    DesignTraceEventType,
    DesignTraceRecord,
    
)


class DesignTraceBuilder:
    """
    Builds consistent design trace records from existing
    proposal and objective state.

    The builder inspects design state only. It does not
    modify the proposal or authoritative exercise design.
    """
    def build_review_started_record(
        self,
        proposal,
    ) -> DesignTraceRecord:
        record = DesignTraceRecord(
            event_type=(
                DesignTraceEventType.REVIEW_STARTED
            ),
            objective_title=proposal.objective_title,
            proposal_id=proposal.proposal_id,
            summary=(
                "Designer review of the design proposal started."
            ),
            rationale=proposal.rationale,
            proposed_content=list(
                proposal.proposed_content
            ),
            reviewed_content=list(
                proposal.reviewed_content
            ),
            recorded_by="Exercise Designer",
        )

        for source in proposal.sources:
            reference = source.source_type

            if source.source_reference:
                reference += (
                    f" — {source.source_reference}"
                )

            record.add_source_reference(
                reference
            )

        record.mark_recorded_now()

        return record
    def build_designer_edited_record(
        self,
        proposal,
    ) -> DesignTraceRecord:
        record = DesignTraceRecord(
            event_type=(
                DesignTraceEventType.DESIGNER_EDITED
            ),
            objective_title=proposal.objective_title,
            proposal_id=proposal.proposal_id,
            summary=(
                "Designer saved a reviewed version "
                "of the design proposal."
            ),
            rationale=proposal.rationale,
            proposed_content=list(
                proposal.proposed_content
            ),
            reviewed_content=list(
                proposal.reviewed_content
            ),
            recorded_by="Exercise Designer",
        )

        for source in proposal.sources:
            reference = source.source_type

            if source.source_reference:
                reference += (
                    f" — {source.source_reference}"
                )

            record.add_source_reference(
                reference
            )

        record.mark_recorded_now()

        return record
    def build_proposal_accepted_record(
        self,
        proposal,
    ) -> DesignTraceRecord:
        record = DesignTraceRecord(
            event_type=(
                DesignTraceEventType.PROPOSAL_ACCEPTED
            ),
            objective_title=proposal.objective_title,
            proposal_id=proposal.proposal_id,
            summary=(
                "Designer accepted the reviewed "
                "design proposal."
            ),
            rationale=proposal.rationale,
            proposed_content=list(
                proposal.proposed_content
            ),
            reviewed_content=list(
                proposal.reviewed_content
            ),
            recorded_by="Exercise Designer",
        )

        for source in proposal.sources:
            reference = source.source_type

            if source.source_reference:
                reference += (
                    f" — {source.source_reference}"
                )

            record.add_source_reference(
                reference
            )

        record.mark_recorded_now()

        return record
    def build_proposal_created_record(
        self,
        proposal,
    ) -> DesignTraceRecord:
        record = DesignTraceRecord(
            event_type=(
                DesignTraceEventType.PROPOSAL_CREATED
            ),
            objective_title=proposal.objective_title,
            proposal_id=proposal.proposal_id,
            summary=(
                "Exercise Director created a "
                "design proposal."
            ),
            rationale=proposal.rationale,
            proposed_content=list(
                proposal.proposed_content
            ),
            recorded_by="Exercise Director",
        )

        for source in proposal.sources:
            reference = source.source_type

            if source.source_reference:
                reference += (
                    f" — {source.source_reference}"
                )

            record.add_source_reference(
                reference
            )

        record.mark_recorded_now()

        return record
    
    def build_applied_record(
        self,
        proposal,
        objective,
    ) -> DesignTraceRecord:
        record = DesignTraceRecord(
            event_type=(
                DesignTraceEventType.APPLIED_TO_DESIGN
            ),
            objective_title=objective.title,
            proposal_id=proposal.proposal_id,
            summary=(
                "Accepted design proposal applied "
                "to authoritative design."
            ),
            rationale=proposal.decision_rationale,
            proposed_content=list(
                proposal.proposed_content
            ),
            reviewed_content=list(
                proposal.reviewed_content
            ),
            resulting_content=list(
                objective.success_criteria
            ),
            recorded_by=proposal.reviewed_by,
        )

        for source in proposal.sources:
            reference = source.source_type

            if source.source_reference:
                reference += (
                    f" — {source.source_reference}"
                )

            record.add_source_reference(
                reference
            )

        record.mark_recorded_now()

        return record