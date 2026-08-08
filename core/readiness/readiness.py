from dataclasses import dataclass, field

from .readiness_gap import ReadinessGap


@dataclass
class OperationalReadiness:
    """
    Describes the readiness that an organisation,
    team or individual is required to achieve.
    """

    current_state: str = ""

    required_state: str = ""

    required_standard: str = ""

    readiness_gap: ReadinessGap = field(
        default_factory=ReadinessGap
    )

    rationale: str = ""