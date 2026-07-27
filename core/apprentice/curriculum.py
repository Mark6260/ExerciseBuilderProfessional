from .lesson import ApprenticeLesson


class ApprenticeCurriculum:
    """
    Defines the professional questions that guide
    an operational readiness conversation.
    """

    def __init__(self):
        self.lessons = [
            ApprenticeLesson(
                lesson_id="001",
                title="Operational Readiness",
                purpose=(
                    "Understand the readiness that the individual, "
                    "team or organisation needs to achieve."
                ),
                question=(
                    "Tell me what operational readiness "
                    "you're trying to achieve."
                ),
                explanation=(
                    "Begin with the required outcome rather than "
                    "the type of exercise or training activity."
                ),
            ),
        ]

        self.current_index = 0

    @property
    def current_lesson(self):
        return self.lessons[self.current_index]