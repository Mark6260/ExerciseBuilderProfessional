from dataclasses import dataclass, field


@dataclass
class NotebookEntry:
    lesson_id: str
    title: str
    answer: str


@dataclass
class ApprenticeNotebook:
    entries: list[NotebookEntry] = field(default_factory=list)

    def record(self, lesson, answer: str):
        self.entries.append(
            NotebookEntry(
                lesson_id=lesson.lesson_id,
                title=lesson.title,
                answer=answer,
            )
        )

    def answer_for(self, lesson_id: str):
        for entry in self.entries:
            if entry.lesson_id == lesson_id:
                return entry.answer

        return ""

    def clear(self):
        self.entries.clear()