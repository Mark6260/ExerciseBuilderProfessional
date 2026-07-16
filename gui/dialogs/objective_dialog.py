from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QTextEdit,
    QVBoxLayout,
)

from core.objective import ExerciseObjective


class ObjectiveDialog(QDialog):
    """
    Collects the basic details for a new exercise objective.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Exercise Objective")
        self.resize(500, 320)

        self.title_input = QLineEdit()
        self.description_input = QTextEdit()

        form = QFormLayout()
        form.addRow("Title:", self.title_input)
        form.addRow("Description:", self.description_input)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.accepted.connect(self.validate_and_accept)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def validate_and_accept(self):
        if not self.title_input.text().strip():
            QMessageBox.warning(
                self,
                "Objective Required",
                "Enter a title for the exercise objective.",
            )
            return

        self.accept()

    def objective(self):
        return ExerciseObjective(
            title=self.title_input.text().strip(),
            description=self.description_input.toPlainText().strip(),
        )