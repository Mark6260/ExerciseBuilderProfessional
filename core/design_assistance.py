from dataclasses import dataclass
from enum import Enum


class DesignAttentionLevel(Enum):
    INFORMATION = "Information"
    ATTENTION = "Needs Attention"


class DesignAttentionType(Enum):
    NO_SUCCESS_CRITERIA = "No Success Criteria"
    NO_SUPPORTING_ACTIVITY = "No Supporting Activity"
    BROKEN_ACTIVITY_LINK = "Broken Activity Link"
    
class DesignOptionType(Enum):
    REVIEW_OBJECTIVE = "Review Objective"
    REVIEW_SUPPORTING_ACTIVITY = "Review Supporting Activity"
    DEFINE_SUCCESS_CRITERIA = "Consider Defining Success Criteria"
    REVIEW_ACTIVITY_LINK = "Review Activity Link"
    CONSIDER_SUPPORTING_ACTIVITY = "Consider Supporting Activity"
    LEAVE_UNCHANGED = "Leave Unchanged"

@dataclass
class DesignOption:
    """
    A possible route the designer may consider in response
    to a design attention item.

    An option does not prescribe an action and does not
    represent a decision by Exercise Director.
    """

    option_type: DesignOptionType
    title: str
    description: str
    
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
    rationale: str = ""

    level: DesignAttentionLevel = (
        DesignAttentionLevel.ATTENTION
    )

    objective_index: int = -1
    objective_title: str = ""

    related_inject_number: int | None = None
    options: list[DesignOption] | None = None
    
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
                    rationale=(
                        "Success criteria connect an exercise objective "
                        "to observable performance and evidence. Without "
                        "them, supporting activity may exist, but the "
                        "design cannot yet establish what successful "
                        "performance should look like or what evidence "
                        "would support assessment."
                    ),
                    options=[
                        DesignOption(
                            option_type=(
                                DesignOptionType.REVIEW_OBJECTIVE
                            ),
                            title="Review the objective",
                            description=(
                                "Check that the objective expresses the "
                                "intended exercise outcome."
                            ),
                        ),
                        DesignOption(
                            option_type=(
                                DesignOptionType.REVIEW_SUPPORTING_ACTIVITY
                            ),
                            title="Review supporting activity",
                            description=(
                                "Examine what the training audience is "
                                "already being asked to demonstrate."
                            ),
                        ),
                        DesignOption(
                            option_type=(
                                DesignOptionType.DEFINE_SUCCESS_CRITERIA
                            ),
                            title="Consider defining success criteria",
                            description=(
                                "Describe the observable performance that "
                                "would demonstrate achievement of the "
                                "objective."
                            ),
                        ),
                        DesignOption(
                            option_type=(
                                DesignOptionType.LEAVE_UNCHANGED
                            ),
                            title="Leave unchanged",
                            description=(
                                "The designer may determine that no change "
                                "is required."
                            ),
                        ),
                    ],
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
                    rationale=(
                        "An exercise objective requires a credible "
                        "opportunity for the training audience to "
                        "demonstrate the required performance. Without "
                        "supporting activity, the objective may not be "
                        "meaningfully exercised or observed."
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
                    rationale=(
                        "The design relationship points to activity that "
                        "is no longer present in the MEL/MIL. This may "
                        "leave the objective without the exercise "
                        "opportunity originally intended to support it."
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