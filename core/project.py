import json
from pathlib import Path

from core.doctrine import DoctrineReference
from core.inject import Inject, InjectStatus
from core.objective import ExerciseObjective
from core.readiness import OperationalRequirement
from core.readiness.readiness import OperationalReadiness
from core.apprentice import ApprenticeNotebook


class Project:
    def __init__(self, name="Untitled Project"):
        self.name = name

        self.operational_requirement = OperationalRequirement()
        self.apprentice_notebook = ApprenticeNotebook()

        self.injects: list[Inject] = []
        self.objectives: list[ExerciseObjective] = []
        self.doctrine_references: list[DoctrineReference] = []

    def add_inject(self, inject: Inject):
        self.injects.append(inject)

    def add_objective(self, objective: ExerciseObjective):
        self.objectives.append(objective)

    def add_doctrine_reference(
        self,
        doctrine_reference: DoctrineReference,
    ):
        self.doctrine_references.append(doctrine_reference)

    def save(self, filename):
        project_data = {
            "name": self.name,

            "operational_requirement": {
                "title": self.operational_requirement.title,
                "description": self.operational_requirement.description,
                "sponsor": self.operational_requirement.sponsor,
                "operational_driver": (
                    self.operational_requirement.operational_driver
                ),
                "success_criteria": (
                    self.operational_requirement.success_criteria
                ),
                "doctrine_reference": (
                    self.operational_requirement.doctrine_reference
                ),

                "readiness": {
                    "current_state": (
                        self.operational_requirement.readiness.current_state
                    ),
                    "required_state": (
                        self.operational_requirement.readiness.required_state
                    ),
                    "required_standard": (
                        self.operational_requirement.readiness.required_standard
                    ),
                    "readiness_gap": (
                        self.operational_requirement.readiness.readiness_gap
                    ),
                    "rationale": (
                        self.operational_requirement.readiness.rationale
                    ),
                },
            },

            "doctrine_references": [
                {
                    "title": doctrine.title,
                    "reference": doctrine.reference,
                    "version": doctrine.version,
                    "organisation": doctrine.organisation,
                    "description": doctrine.description,
                    "location": doctrine.location,
                }
                for doctrine in self.doctrine_references
            ],

            "objectives": [
                {
                    "title": objective.title,
                    "description": objective.description,
                    "success_criteria": objective.success_criteria,
                    "supporting_injects": objective.supporting_injects,
                    "achieved": objective.achieved,
                }
                for objective in self.objectives
            ],

            "injects": [
                {
                    "number": inject.number,
                    "title": inject.title,
                    "exercise_time": inject.exercise_time,
                    "phase": inject.phase,
                    "source": inject.source,
                    "method": inject.method,
                    "audience": inject.audience,
                    "category": inject.category,
                    "inject_text": inject.inject_text,
                    "expected_action": inject.expected_action,
                    "facilitator_notes": inject.facilitator_notes,
                    "attachments": inject.attachments,
                    "status": inject.status.value,
                }
                for inject in self.injects
            ],
        }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(project_data, file, indent=4)

    @classmethod
    def load(cls, filename):
        path = Path(filename)

        if not path.exists():
            raise FileNotFoundError("Project file not found")

        with open(filename, "r", encoding="utf-8") as file:
            project_data = json.load(file)

        project = cls(
            project_data.get("name", "Untitled Project")
        )

        saved_operational_requirement = project_data.get(
            "operational_requirement",
            {},
        )

        saved_readiness = saved_operational_requirement.get(
            "readiness",
            {},
        )

        project.operational_requirement = OperationalRequirement(
            title=saved_operational_requirement.get("title", ""),
            description=saved_operational_requirement.get(
                "description",
                "",
            ),
            sponsor=saved_operational_requirement.get("sponsor", ""),
            operational_driver=saved_operational_requirement.get(
                "operational_driver",
                "",
            ),
            success_criteria=saved_operational_requirement.get(
                "success_criteria",
                "",
            ),
            doctrine_reference=saved_operational_requirement.get(
                "doctrine_reference"
            ),
            readiness=OperationalReadiness(
                current_state=saved_readiness.get(
                    "current_state",
                    "",
                ),
                required_state=saved_readiness.get(
                    "required_state",
                    "",
                ),
                required_standard=saved_readiness.get(
                    "required_standard",
                    "",
                ),
                readiness_gap=saved_readiness.get(
                    "readiness_gap",
                    "",
                ),
                rationale=saved_readiness.get(
                    "rationale",
                    "",
                ),
            ),
        )

        saved_doctrine_references = project_data.get(
            "doctrine_references",
            [],
        )

        project.doctrine_references = [
            DoctrineReference(
                title=item.get("title", ""),
                reference=item.get("reference", ""),
                version=item.get("version", ""),
                organisation=item.get("organisation", ""),
                description=item.get("description", ""),
                location=item.get("location", ""),
            )
            for item in saved_doctrine_references
        ]

        saved_objectives = project_data.get(
            "objectives",
            [],
        )

        project.objectives = [
            ExerciseObjective(
                title=item.get("title", ""),
                description=item.get("description", ""),
                success_criteria=item.get(
                    "success_criteria",
                    [],
                ),
                supporting_injects=item.get(
                    "supporting_injects",
                    [],
                ),
                achieved=item.get("achieved"),
            )
            for item in saved_objectives
        ]

        saved_injects = project_data.get(
            "injects",
            project_data.get("exercises", []),
        )

        project.injects = [
            Inject(
                number=item.get("number", 0),
                title=item.get("title", ""),
                exercise_time=item.get(
                    "exercise_time",
                    "",
                ),
                phase=item.get("phase", ""),
                source=item.get("source", ""),
                method=item.get("method", ""),
                audience=item.get("audience", ""),
                category=item.get("category", ""),
                inject_text=item.get(
                    "inject_text",
                    "",
                ),
                expected_action=item.get(
                    "expected_action",
                    "",
                ),
                facilitator_notes=item.get(
                    "facilitator_notes",
                    "",
                ),
                attachments=item.get(
                    "attachments",
                    [],
                ),
                status=cls._parse_status(
                    item.get(
                        "status",
                        InjectStatus.PLANNED.value,
                    )
                ),
            )
            for item in saved_injects
        ]

        return project

    @staticmethod
    def _parse_status(value):
        for status in InjectStatus:
            if status.value == value:
                return status

        return InjectStatus.PLANNED