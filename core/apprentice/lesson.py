from dataclasses import dataclass


@dataclass
class ApprenticeLesson:
    """
    A professional lesson taught to the Apprentice.

    Each lesson explains what the Apprentice needs to understand,
    why it matters and what question it should ask.
    """

    lesson_id: str
    title: str
    purpose: str
    question: str
    explanation: str = ""