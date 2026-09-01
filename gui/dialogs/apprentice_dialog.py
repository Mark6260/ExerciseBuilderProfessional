from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)

from core.apprentice import ApprenticeCurriculum
from core.language import ExerciseDirector


class ApprenticeDialog(QDialog):
    """
    Presents the first professional question, captures the answer,
    and confirms what the Apprentice has understood.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("The Apprentice")
        self.setMinimumWidth(620)
        self.resize(720, 620)

        self.curriculum = ApprenticeCurriculum()
        self.lesson = self.curriculum.current_lesson
        self.profession = ExerciseDirector

        self.answer_text = ""
        self.answer_confirmed = False

        self.title_label = QLabel(
            "Welcome to the Workshop."
        )
        self.title_label.setStyleSheet(
            "font-size: 22px; font-weight: bold;"
        )

        self.introduction_label = QLabel(
            "I'm your Apprentice.\n\n"
            "I won't replace your experience.\n"
            "I won't make operational decisions.\n"
            "I won't tell you how to run your exercise.\n\n"
            "I'll ask the questions that help experienced "
            "Exercise Directors think."
        )
        self.introduction_label.setWordWrap(True)

        self.lesson_heading = QLabel(
            f"Lesson {self.lesson.lesson_id}: "
            f"{self.lesson.title}"
        )
        self.lesson_heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.lesson_purpose = QLabel(
            self.lesson.purpose
        )
        self.lesson_purpose.setWordWrap(True)

        self.lesson_question = QLabel(
            f"<b>{self.profession.lesson_001_question}</b>"
        )
        self.lesson_question.setWordWrap(True)
        self.lesson_question.setStyleSheet(
            "font-size: 17px;"
        )

        self.answer_input = QPlainTextEdit()
        self.answer_input.setPlaceholderText(
            "Describe the required outcome, capability "
            "or level of readiness..."
        )
        
        self.answer_input.setMinimumHeight(160)

        self.lesson_explanation = QLabel(
            self.lesson.explanation
        )
        self.lesson_explanation.setWordWrap(True)

        self.acknowledgement_label = QLabel()
        self.acknowledgement_label.setWordWrap(True)
        self.acknowledgement_label.setStyleSheet(
            "font-size: 16px;"
        )
        self.acknowledgement_label.hide()

        self.continue_button = QPushButton(
            "Record Requirement"
        )
        self.continue_button.clicked.connect(
            self.continue_conversation
        )

        layout = QVBoxLayout()
        layout.setSpacing(12)

        layout.addWidget(self.title_label)
        layout.addWidget(self.introduction_label)
        layout.addSpacing(8)
        layout.addWidget(self.lesson_heading)
        layout.addWidget(self.lesson_purpose)
        layout.addWidget(self.lesson_question)
        layout.addWidget(self.answer_input)
        layout.addWidget(self.lesson_explanation)
        layout.addWidget(self.acknowledgement_label)
        layout.addStretch()
        layout.addWidget(
            self.continue_button,
            alignment=Qt.AlignmentFlag.AlignRight,
        )

        self.setLayout(layout)

    def continue_conversation(self):
        if self.answer_confirmed:
            self.accept()
            return

        self.answer_text = (
            self.answer_input
            .toPlainText()
            .strip()
        )
        self.notebook_summary = (
            "✓ Mission\n\n"
            f"    {self.answer_text}"
        )

        if not self.answer_text:
            self.answer_input.setFocus()
            return

        self.answer_confirmed = True

        self.lesson_question.hide()
        self.answer_input.hide()
        self.lesson_explanation.hide()

        self.acknowledgement_label.setText(
            "<b>Understood.</b><br><br>"
            "Requirement recorded:<br><br>"
            f"{self.answer_text}<br><br>"
            "Let's now examine the readiness required "
            "to achieve this outcome."
        )
        self.acknowledgement_label.show()

        self.continue_button.setText(
            "Continue to Readiness Analysis"
        )

    def answer(self):
        return self.answer_text