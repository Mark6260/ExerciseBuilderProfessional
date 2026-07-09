from dataclasses import dataclass, field


@dataclass
class Exercise:
    title: str = ""
    question: str = ""
    answers: list[str] = field(default_factory=list)
    correct_answers: list[int] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self):
        return {
            "title": self.title,
            "question": self.question,
            "answers": self.answers,
            "correct_answers": self.correct_answers,
            "images": self.images,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get("title", ""),
            question=data.get("question", ""),
            answers=data.get("answers", []),
            correct_answers=data.get("correct_answers", []),
            images=data.get("images", []),
            notes=data.get("notes", ""),
        )

    def __str__(self):
        return self.title or "Untitled Exercise"