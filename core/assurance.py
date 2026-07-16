from dataclasses import dataclass

from core.project import Project


@dataclass
class AssuranceFinding:
    severity: str
    category: str
    item: str
    message: str
    recommendation: str


class ExerciseAssurance:
    """
    Performs evidence-based assurance checks against an exercise project.

    The engine records facts about missing or incomplete information.
    It does not judge whether an exercise is good or bad.
    """

    def __init__(self, project: Project):
        self.project = project

    def check(self):
        """
        Return a summary and a list of actionable assurance findings.
        """

        findings = []

        findings.extend(self.check_project())
        findings.extend(self.check_injects())

        return {
            "project_name": self.project.name,
            "inject_count": len(self.project.injects),
            "finding_count": len(findings),
            "findings": findings,
        }

    def check_project(self):
        findings = []

        if not self.project.name.strip():
            findings.append(
                AssuranceFinding(
                    severity="Critical",
                    category="Exercise",
                    item="Exercise name",
                    message="The exercise does not have a name.",
                    recommendation=(
                        "Give the exercise a clear name before delivery."
                    ),
                )
            )

        if not self.project.injects:
            findings.append(
                AssuranceFinding(
                    severity="Critical",
                    category="Master Events List",
                    item="Injects",
                    message=(
                        "The exercise does not contain any injects."
                    ),
                    recommendation=(
                        "Import or create the Master Events List before "
                        "delivery."
                    ),
                )
            )

        return findings

    def check_injects(self):
        findings = []

        for inject in self.project.injects:
            item_name = self._inject_name(inject)

            if not inject.title.strip():
                findings.append(
                    AssuranceFinding(
                        severity="Critical",
                        category="Inject",
                        item=item_name,
                        message="The inject title is missing.",
                        recommendation=(
                            "Add a clear title so the inject can be "
                            "identified."
                        ),
                    )
                )

            if not inject.exercise_time.strip():
                findings.append(
                    AssuranceFinding(
                        severity="Critical",
                        category="Master Events List",
                        item=item_name,
                        message="The inject does not have an exercise time.",
                        recommendation=(
                            "Assign an exercise time so the planned sequence "
                            "can be reproduced."
                        ),
                    )
                )

            if not inject.inject_text.strip():
                findings.append(
                    AssuranceFinding(
                        severity="Critical",
                        category="Inject",
                        item=item_name,
                        message="The inject content is missing.",
                        recommendation=(
                            "Add the information that will be issued to "
                            "participants."
                        ),
                    )
                )

            if not inject.expected_action.strip():
                findings.append(
                    AssuranceFinding(
                        severity="Advisory",
                        category="Inject",
                        item=item_name,
                        message="The expected action is missing.",
                        recommendation=(
                            "Define the intended training response or "
                            "learning opportunity."
                        ),
                    )
                )

            if not inject.category.strip():
                findings.append(
                    AssuranceFinding(
                        severity="Advisory",
                        category="Master Events List",
                        item=item_name,
                        message="The inject category is missing.",
                        recommendation=(
                            "Assign a category if it is required by the "
                            "exercise design."
                        ),
                    )
                )

        return findings

    @staticmethod
    def _inject_name(inject):
        if inject.number and inject.title:
            return f"Inject {inject.number}: {inject.title}"

        if inject.number:
            return f"Inject {inject.number}"

        if inject.title:
            return inject.title

        return "Unidentified inject"