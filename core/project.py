import json
from pathlib import Path

from core.inject import Inject, InjectStatus
from core.objective import ExerciseObjective


class Project:
    def __init__(self, name="Untitled Project"):
        self.name = name

        self.injects: list[Inject] = []

        self.objectives: list[ExerciseObjective] = []

    def add_inject(self, inject: Inject):
        self.injects.append(inject)

    def save(self, filename):
        project_data = {
            "name": self.name,
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

        project = cls(project_data.get("name", "Untitled Project"))

        saved_items = project_data.get(
            "injects",
            project_data.get("exercises", []),
        )

        project.injects = [
            Inject(
                number=item.get("number", 0),
                title=item.get("title", ""),
                exercise_time=item.get("exercise_time", ""),
                phase=item.get("phase", ""),
                source=item.get("source", ""),
                method=item.get("method", ""),
                audience=item.get("audience", ""),
                category=item.get("category", ""),
                inject_text=item.get("inject_text", ""),
                expected_action=item.get("expected_action", ""),
                facilitator_notes=item.get("facilitator_notes", ""),
                attachments=item.get("attachments", []),
                status=cls._parse_status(
                    item.get("status", InjectStatus.PLANNED.value)
                ),
            )
            for item in saved_items
        ]

        return project

    @staticmethod
    def _parse_status(value):
        for status in InjectStatus:
            if status.value == value:
                return status

        return InjectStatus.PLANNED