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

    Pre-delivery design assurance findings remain separate from the
    evidence, assessment and authorised readiness-decision trail.
    """

    def __init__(self, project: Project):
        self.project = project

    def check(self):
        """
        Return design-assurance findings plus a factual summary of the
        evidence, assessment and authorised readiness-decision trail.
        """

        findings = []

        findings.extend(self.check_project())
        findings.extend(self.check_objectives())
        findings.extend(self.check_injects())

        return {
            "project_name": self.project.name,
            "inject_count": len(self.project.injects),
            "objective_count": len(self.project.objectives),
            "finding_count": len(findings),
            "findings": findings,
            "performance_assurance": (
                self.performance_assurance_summary()
            ),
        }

    def performance_assurance_summary(self):
        """
        Report facts about the post-conduct assurance chain.

        This method does not infer readiness from observations, evidence
        or assessment outcomes. It only reports what has been recorded.
        """

        observations = getattr(
            self.project,
            "observations",
            [],
        )

        evidence_records = getattr(
            self.project,
            "evidence_records",
            [],
        )

        assessment_records = getattr(
            self.project,
            "assessment_records",
            [],
        )

        readiness_decisions = getattr(
            self.project,
            "readiness_decisions",
            [],
        )

        reviewed_observation_count = sum(
            getattr(
                getattr(observation, "status", None),
                "value",
                "",
            )
            == "Reviewed"
            for observation in observations
        )

        latest_decision = (
            readiness_decisions[-1]
            if readiness_decisions
            else None
        )

        return {
            "observation_count": len(observations),
            "reviewed_observation_count": (
                reviewed_observation_count
            ),
            "evidence_count": len(evidence_records),
            "assessment_count": len(assessment_records),
            "readiness_decision_count": len(
                readiness_decisions
            ),
            "readiness_outcome": (
                latest_decision.outcome.value
                if latest_decision is not None
                else ""
            ),
            "decision_maker": (
                latest_decision.decision_maker
                if latest_decision is not None
                else ""
            ),
            "decision_authority": (
                latest_decision.decision_authority
                if latest_decision is not None
                else ""
            ),
            "recorded_at": (
                latest_decision.recorded_at
                if latest_decision is not None
                else ""
            ),
            "limitations": (
                latest_decision.limitations
                if latest_decision is not None
                else ""
            ),
            "required_action": (
                latest_decision.required_action
                if latest_decision is not None
                else ""
            ),
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

    def check_objectives(self):
        findings = []

        if not self.project.objectives:
            findings.append(
                AssuranceFinding(
                    severity="Advisory",
                    category="Exercise Design",
                    item="Exercise objectives",
                    message=(
                        "No exercise objectives have been defined."
                    ),
                    recommendation=(
                        "Define one or more measurable objectives that "
                        "describe what the exercise is intended to achieve."
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
                        message=(
                            "The inject does not have an exercise time."
                        ),
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
