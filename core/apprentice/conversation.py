from .curriculum import ApprenticeCurriculum
from .notebook import ApprenticeNotebook
from core.language import BritishArmy


class ApprenticeConversation:

    def __init__(self):

        self.curriculum = ApprenticeCurriculum()
        self.notebook = ApprenticeNotebook()
        self.profession = BritishArmy

    @property
    def lesson(self):
        return self.curriculum.current_lesson

    @property
    def question(self):
        return self.profession.lesson_001_question

    def record_mission(self, mission):

        self.notebook.record(
            "Mission",
            mission,
        )

        return (
            "Understood.\n\n"
            f"You're preparing:\n\n{mission}\n\n"
            "We'll use this mission as the foundation "
            "for the readiness case."
        )