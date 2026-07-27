from dataclasses import dataclass


@dataclass
class OperationalReadiness:
    """
    Describes the readiness that an organisation,
    team or individual is required to achieve.
    """

    current_state: str = ""

    required_state: str = ""

    required_standard: str = ""

    readiness_gap: str = ""

    rationale: str = ""