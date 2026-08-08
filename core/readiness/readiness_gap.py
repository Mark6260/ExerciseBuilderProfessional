from dataclasses import dataclass


@dataclass
class ReadinessGap:
    """
    Describes an identified gap between the required readiness
    standard and the current evidenced state.

    A ReadinessGap does not determine whether an organisation,
    team or individual is ready. It records the shortfall that
    must be considered by the appropriate professional authority.
    """

    required_standard: str = ""

    current_state: str = ""

    shortfall: str = ""

    consequence: str = ""

    preparation_requirement: str = ""

    rationale: str = ""