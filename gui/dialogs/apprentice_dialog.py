from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from core.apprentice import ApprenticeCurriculum


class ApprenticeDialog(QDialog):
    """
    Introduces the Apprentice and presents the first
    lesson from the Exercise Director curriculum.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("The Apprentice")
        self.setMinimumWidth(560)

        self.curriculum = ApprenticeCurriculum()
        lesson = self.curriculum.current_lesson

        title = QLabel("Welcome to the Workshop.")
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold;"
        )

        introduction = QLabel(
            "I'm your Apprentice.\n\n"
            "I won't replace your experience.\n"
            "I won't make operational decisions.\n"
            "I won't tell you how to run your exercise.\n\n"
            "I'll ask the questions that experienced "
            "Exercise Directors ask themselves."
        )
        introduction.setWordWrap(True)

        lesson_heading = QLabel(
            f"Lesson {lesson.lesson_id}: {lesson.title}"
        )
        lesson_heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        lesson_purpose = QLabel(lesson.purpose)
        lesson_purpose.setWordWrap(True)

        lesson_question = QLabel(
            f"<b>{lesson.question}</b>"
        )
        lesson_question.setWordWrap(True)
        lesson_question.setStyleSheet(
            "font-size: 17px;"
        )

        lesson_explanation = QLabel(
            lesson.explanation
        )
        lesson_explanation.setWordWrap(True)

        begin_button = QPushButton(
            "Begin the Conversation"
        )
        begin_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.setSpacing(12)

        layout.addWidget(title)
        layout.addWidget(introduction)
        layout.addSpacing(8)
        layout.addWidget(lesson_heading)
        layout.addWidget(lesson_purpose)
        layout.addWidget(lesson_question)
        layout.addWidget(lesson_explanation)
        layout.addStretch()
        layout.addWidget(
            begin_button,
            alignment=Qt.AlignmentFlag.AlignRight,
        )

        self.setLayout(layout)