from dataclasses import dataclass
from enum import Enum


class DesignAttentionLevel(Enum):
    INFORMATION = "Information"
    ATTENTION = "Needs Attention"


class DesignAttentionType(Enum):
    NO_SUCCESS_CRITERIA = "No Success Criteria"
    NO_SUPPORTING_ACTIVITY = "No Supporting Activity"
    BROKEN_ACTIVITY_LINK = "Broken Activity Link"


@dataclass
class DesignAttentionItem:
    """
    Records a design matter that may require professional
    attention.

    An attention item is derived from the current exercise
    design. It does not make a professional judgement and
    does not prevent the designer from continuing.
    """

    attention_type: DesignAttentionType
    title: str
    message: str

    level: DesignAttentionLevel = (
        DesignAttentionLevel.ATTENTION
    )

    objective_index: int = -1
    objective_title: str = ""

    related_inject_number: int | None = None
class DesignAssistance:
    """
    Reviews the current exercise design for matters that
    may require professional attention.

    DesignAssistance identifies observable design conditions.
    It does not make professional judgements or prevent the
    designer from continuing.
    """

    def __init__(self, project):
        self.project = project

    def check(self) -> list[DesignAttentionItem]:
        items: list[DesignAttentionItem] = []

        for objective_index, objective in enumerate(
            self.project.objectives
        ):
            items.extend(
                self._check_objective(
                    objective_index,
                    objective,
                )
            )

        return items

    def _check_objective(
        self,
        objective_index,
        objective,
    ) -> list[DesignAttentionItem]:
        items: list[DesignAttentionItem] = []

        objective_title = (
            objective.title.strip()
            or "Untitled objective"
        )

        success_criteria = getattr(
            objective,
            "success_criteria",
            [],
        )

        supporting_injects = getattr(
            objective,
            "supporting_injects",
            [],
        )

        if not success_criteria:
            items.append(
                DesignAttentionItem(
                    attention_type=(
                        DesignAttentionType.NO_SUCCESS_CRITERIA
                    ),
                    title="Success criteria not defined",
                    message=(
                        "Exercise Director cannot yet determine "
                        "what successful demonstration of this "
                        "objective looks like."
                    ),
                    objective_index=objective_index,
                    objective_title=objective_title,
                )
            )

        if not supporting_injects:
            items.append(
                DesignAttentionItem(
                    attention_type=(
                        DesignAttentionType.NO_SUPPORTING_ACTIVITY
                    ),
                    title="No supporting activity identified",
                    message=(
                        "No MEL/MIL activity is currently linked "
                        "to provide an opportunity to exercise "
                        "this objective."
                    ),
                    objective_index=objective_index,
                    objective_title=objective_title,
                )
            )

            return items

        available_inject_numbers = {
            inject.number
            for inject in self.project.injects
        }

        for inject_number in supporting_injects:
            if inject_number in available_inject_numbers:
                continue

            items.append(
                DesignAttentionItem(
                    attention_type=(
                        DesignAttentionType.BROKEN_ACTIVITY_LINK
                    ),
                    title="Supporting activity cannot be found",
                    message=(
                        f"Inject {inject_number} is linked to "
                        "this objective but is not present in "
                        "the current MEL/MIL."
                    ),
                    objective_index=objective_index,
                    objective_title=objective_title,
                    related_inject_number=inject_number,
                )
            )

        return items