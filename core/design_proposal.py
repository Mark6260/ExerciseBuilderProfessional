from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class DesignProposalType(Enum):
    SUCCESS_CRITERIA = "Success Criteria"


class DesignProposalStatus(Enum):
    DRAFT = "Draft"
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

    sources: list[DesignProposalSource] = field(
        default_factory=list
    )

    rationale: str = ""

    status: DesignProposalStatus = (
        DesignProposalStatus.DRAFT
    )

    def add_proposed_content(self, content: str):
        content = content.strip()

        if content and content not in self.proposed_content:
            self.proposed_content.append(content)

    def add_source(
        self,
        source: DesignProposalSource,
    ):
        self.sources.append(source)