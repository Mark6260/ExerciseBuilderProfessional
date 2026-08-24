from enum import Enum


class PreparednessScope(Enum):
    """
    Identifies the level at which a preparedness record applies.

    Scope describes whose preparedness, learning or demonstrated
    strength is being recorded. It does not itself make a
    preparedness or readiness judgement.
    """

    INDIVIDUAL = "Individual"
    TEAM = "Team"
    COLLECTIVE = "Collective"