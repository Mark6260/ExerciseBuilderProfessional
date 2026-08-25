from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class DesignProposalType(Enum):
    SUCCESS_CRITERIA = "Success Criteria"


class DesignProposalStatus(Enum):
    DRAFT = "Draft"
    UNDER_REVIEW = "Under Review"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"


@dataclass
class DesignProposalSource:
    """
    Identifies existing design material that informed
    a proposal.
    """

    source_type: str
    source_reference: str
    source_text: str = ""


@dataclass
class DesignProposal:
    """
    Holds proposed design content separately from the
    authoritative exercise design.

    A proposal remains non-authoritative until explicitly
    accepted by the designer.
    """

    proposal_type: DesignProposalType
    objective_title: str

    proposal_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    proposed_content: list[str] = field(
        default_factory=list
    )
    reviewed_content: list[str] = field(
        default_factory=list
    )

    sources: list[DesignProposalSource] = field(
        default_factory=list
    )

    rationale: str = ""

    status: DesignProposalStatus = (
        DesignProposalStatus.DRAFT
        
    )
    reviewed_by: str = ""
    decision_rationale: str = ""
    
    def add_proposed_content(self, content: str):
        content = content.strip()

        if content and content not in self.proposed_content:
            self.proposed_content.append(content)

    def add_source(
        self,
        source: DesignProposalSource,
    ):
        self.sources.append(source)
    def begin_review(self):
        """
        Begin designer review without altering the original
        Exercise Director proposal.
        """

        if self.status is not DesignProposalStatus.DRAFT:
            return

        self.reviewed_content = list(
            self.proposed_content
        )

        self.status = (
            DesignProposalStatus.UNDER_REVIEW
        )

    def replace_reviewed_content(
        self,
        content: list[str],
    ):
        """
        Replace the designer's working copy while preserving
        the original proposed content.
        """

        if (
            self.status
            is not DesignProposalStatus.UNDER_REVIEW
        ):
            return

        cleaned_content = []

        for item in content:
            cleaned = item.strip()

            if cleaned and cleaned not in cleaned_content:
                cleaned_content.append(cleaned)

        self.reviewed_content = cleaned_content

    def accept(
        self,
        reviewed_by: str,
        rationale: str = "",
    ):
        """
        Record the designer's acceptance of the reviewed
        content.

        This does not amend the authoritative exercise design.
        """

        if (
            self.status
            is not DesignProposalStatus.UNDER_REVIEW
        ):
            return

        self.reviewed_by = reviewed_by.strip()
        self.decision_rationale = rationale.strip()

        self.status = (
            DesignProposalStatus.ACCEPTED
        )

    def reject(
        self,
        reviewed_by: str,
        rationale: str = "",
    ):
        """
        Record the designer's rejection of the proposal.

        Rejection does not amend the authoritative exercise
        design.
        """

        if self.status not in (
            DesignProposalStatus.DRAFT,
            DesignProposalStatus.UNDER_REVIEW,
        ):
            return

        self.reviewed_by = reviewed_by.strip()
        self.decision_rationale = rationale.strip()

        self.status = (
            DesignProposalStatus.REJECTED
        )