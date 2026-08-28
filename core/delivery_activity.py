from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class DeliveryActivityType(Enum):
    INJECT_ISSUED = "Inject Issued"
    PLAYER_COMMUNICATION = "Player Communication"
    EXCON_ROLEPLAY_RESPONSE = "ExCon Role-Play Response"
    PLAYER_ACTION = "Player Action"
    PLAYER_DECISION = "Player Decision"
    PRODUCT_RECEIVED = "Product Received"
    EXCON_INTERVENTION = "ExCon Intervention"
    INFORMATION_PROVIDED = "Information Provided"
    OTHER_ACTIVITY = "Other Activity"


@dataclass
class DeliveryActivity:
    """
    Records one factual occurrence during live exercise delivery.

    An activity may relate to a planned inject, but does not have
    to. Recording an activity does not assess player performance
    or alter the authoritative exercise design.
    """

    activity_type: DeliveryActivityType
    timestamp: str

    activity_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    from_party: str = ""
    to_party: str = ""
    method: str = ""
    summary: str = ""
    recorded_by: str = ""

    related_inject_number: int | None = None
    related_objective_ids: list[str] = field(
        default_factory=list
    )