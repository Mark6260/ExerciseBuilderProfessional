from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)


class ExerciseDefinitionDialog(QDialog):
    """
    Guides the Exercise Director through defining an exercise
    before detailed design begins.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Mission Analysis")
        self.resize(760, 580)

        workflow_label = QLabel(
            "<b>Mission Analysis</b><br>"
            "Step 1 of 8"
        )

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 8)
        self.progress_bar.setValue(1)
        self.progress_bar.setTextVisible(False)

        title = QLabel(
            "<h2>Why are we conducting this exercise?</h2>"
        )

        guidance = QLabel(
            "Describe the operational problem, capability gap or "
            "training need that this exercise has been designed "
            "to address.\n\n"
            "Focus on what the training audience cannot yet do "
            "confidently, consistently or to the required standard."
        )
        guidance.setWordWrap(True)

        example = QLabel(
            "<b>Example</b><br><br>"
            "The training audience has not recently practised "
            "coordinating a multi-agency response to a prolonged "
            "loss of national power infrastructure.<br><br>"
            "Senior leaders require confidence that the organisation "
            "can establish command, maintain situational awareness "
            "and coordinate recovery activity."
        )
        example.setWordWrap(True)

        problem_label = QLabel(
            "<b>Operational Problem Statement</b>"
        )

        self.training_problem_input = QTextEdit()
        self.training_problem_input.setPlaceholderText(
            "Describe the operational problem, training need or "
            "capability gap..."
        )

        continue_button = QPushButton(
            "Continue Mission Analysis"
        )
        continue_button.clicked.connect(
            self.validate_and_accept
        )

        layout = QVBoxLayout()

        layout.addWidget(workflow_label)
        layout.addWidget(self.progress_bar)
        layout.addSpacing(12)

        layout.addWidget(title)
        layout.addWidget(guidance)
        layout.addWidget(example)
        layout.addSpacing(8)

        layout.addWidget(problem_label)
        layout.addWidget(
            self.training_problem_input,
            1,
        )

        layout.addWidget(continue_button)

        self.setLayout(layout)

    def validate_and_accept(self):
        training_problem = (
            self.training_problem_input
            .toPlainText()
            .strip()
        )

        if not training_problem:
            self.training_problem_input.setFocus()
            return

        self.accept()

    def training_problem(self):
        return (
            self.training_problem_input
            .toPlainText()
            .strip()
        )