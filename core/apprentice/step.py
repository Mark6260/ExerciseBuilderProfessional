from dataclasses import dataclass


@dataclass
class ConversationStep:
    title: str
    question: str
    explanation: str = ""