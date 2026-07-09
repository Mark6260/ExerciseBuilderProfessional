from dataclasses import dataclass, field


@dataclass
class Inject:
    number: int = 0
    title: str = ""
    exercise_time: str = ""
    phase: str = ""
    source: str = ""
    method: str = ""
    audience: str = ""
    category: str = ""

    inject_text: str = ""
    expected_action: str = ""
    facilitator_notes: str = ""

    attachments: list[str] = field(default_factory=list)

    def __str__(self):
        if self.title:
            return f"{self.number}. {self.title}"
        return f"Inject {self.number}"