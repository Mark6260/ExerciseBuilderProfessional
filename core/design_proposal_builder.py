from core.design_proposal import (
    DesignProposal,
    DesignProposalSource,
    DesignProposalType,
)


class DesignProposalBuilder:
    """
    Builds draft design proposals from existing exercise
    design material.

    The builder creates candidate content only. It does not
    amend the authoritative exercise design.
    """

    def __init__(self, project):
        self.project = project

    def build_success_criteria_proposal(
        self,
        objective,
    ) -> DesignProposal:
        proposal = DesignProposal(
            proposal_type=(
                DesignProposalType.SUCCESS_CRITERIA
            ),
            objective_title=objective.title,
        )

        proposal.add_source(
            DesignProposalSource(
                source_type="Objective",
                source_reference=objective.title,
                source_text=objective.title,
            )
        )

        supporting_injects = getattr(
            objective,
            "supporting_injects",
            [],
        )

        for inject_number in supporting_injects:
            inject = self._find_inject(
                inject_number
            )

            if inject is None:
                continue

            expected_action = (
                getattr(
                    inject,
                    "expected_action",
                    "",
                )
                or ""
            ).strip()

            proposal.add_source(
                DesignProposalSource(
                    source_type="Supporting Activity",
                    source_reference=(
                        f"Inject {inject.number}"
                    ),
                    source_text=inject.title,
                )
            )

            if not expected_action:
                continue

            proposal.add_source(
                DesignProposalSource(
                    source_type="Expected Action",
                    source_reference=(
                        f"Inject {inject.number}"
                    ),
                    source_text=expected_action,
                )
            )

            proposal.add_proposed_content(
                expected_action
            )

        proposal.rationale = (
            "Drafted from observable performance already "
            "described in supporting MEL/MIL activity. "
            "The designer should review and refine the "
            "candidate criteria before any acceptance."
        )

        return proposal

    def _find_inject(self, inject_number):
        for inject in self.project.injects:
            if inject.number == inject_number:
                return inject

        return None