from dataclasses import dataclass, field
from typing import Optional

from .readiness import OperationalReadiness


@dataclass
class OperationalRequirement:
    """
    Why does this operational readiness requirement exist?
    """

    title: str = ""

    description: str = ""

    sponsor: str = ""

    operational_driver: str = ""

    success_criteria: str = ""

    doctrine_reference: Optional[str] = None

    readiness: OperationalReadiness = field(
        default_factory=OperationalReadiness
    )