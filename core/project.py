import json
from pathlib import Path


class Project:
    def __init__(self, name="Untitled Exercise Project"):
        self.name = name
        self.exercises = []

    def add_exercise(self, exercise):
        self.exercises.append(exercise)

    def save(self, filename):
        project_data = {
            "name": self.name,
            "exercises": self.exercises
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

        project = cls(project_data.get("name", "Untitled Exercise Project"))
        project.exercises = project_data.get("exercises", [])

        return project