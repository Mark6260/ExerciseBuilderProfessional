from core.design_proposal import (
    DesignProposalStatus,
    DesignProposalType,
)


class DesignProposalApplier:
    """
    Applies an explicitly accepted design proposal to the
    authoritative exercise design.

    Proposal review and proposal application remain separate
    operations.
    """

    def apply(
        self,
        proposal,
        objective,
    ):
        if (
            proposal.status
            is not DesignProposalStatus.ACCEPTED
        ):
            raise ValueError(
                "Only an accepted design proposal "
                "can be applied."
            )

        if (
            proposal.proposal_type
            is not DesignProposalType.SUCCESS_CRITERIA
        ):
            raise ValueError(
                "Unsupported design proposal type."
            )

        if (
            proposal.objective_title
            != objective.title
        ):
            raise ValueError(
                "The proposal does not relate to "
                "this objective."
            )

        if not proposal.reviewed_content:
            raise ValueError(
                "The accepted proposal contains no "
                "reviewed content to apply."
            )

        objective.success_criteria = list(
            proposal.reviewed_content
        )