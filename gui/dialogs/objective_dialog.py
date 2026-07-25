from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QTextEdit,
    QVBoxLayout,
)

from core.objective import ExerciseObjective


class ObjectiveDialog(QDialog):
    """
    Collects the details for a new exercise objective.
    """

    def __init__(
        self,
        injects,
        doctrine_references,
        parent=None,
    ):
        super().__init__(parent)

        self.injects = injects
        self.doctrine_references = doctrine_references

        self.setWindowTitle("Add Exercise Objective")
        self.resize(560, 620)

        self.title_input = QLineEdit()
        self.description_input = QTextEdit()

        form = QFormLayout()
        form.addRow("Title:", self.title_input)
        form.addRow("Description:", self.description_input)

        self.injects_label = QLabel(
            "Injects that assess this objective"
        )
        self.injects_list = QListWidget()

        for inject in self.injects:
            item = QListWidgetItem(
                f"{inject.number}. "
                f"{inject.title or 'Untitled inject'}"
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                inject.number,
            )

            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
            )

            item.setCheckState(
                Qt.CheckState.Unchecked
            )

            self.injects_list.addItem(item)

        self.doctrine_label = QLabel(
            "Doctrine that supports this objective"
        )
        self.doctrine_list = QListWidget()

        for doctrine in self.doctrine_references:
            item = QListWidgetItem(
                doctrine.title or "Untitled doctrine reference"
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                doctrine.title,
            )

            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
            )

            item.setCheckState(
                Qt.CheckState.Unchecked
            )

            self.doctrine_list.addItem(item)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.accepted.connect(
            self.validate_and_accept
        )
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)

        layout.addWidget(self.injects_label)
        layout.addWidget(self.injects_list)

        layout.addWidget(self.doctrine_label)
        layout.addWidget(self.doctrine_list)

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

    def selected_inject_numbers(self):
        selected_numbers = []

        for index in range(self.injects_list.count()):
            item = self.injects_list.item(index)

            if item.checkState() == Qt.CheckState.Checked:
                selected_numbers.append(
                    item.data(Qt.ItemDataRole.UserRole)
                )

        return selected_numbers

    def selected_doctrine_titles(self):
        selected_titles = []

        for index in range(self.doctrine_list.count()):
            item = self.doctrine_list.item(index)

            if item.checkState() == Qt.CheckState.Checked:
                selected_titles.append(
                    item.data(Qt.ItemDataRole.UserRole)
                )

        return selected_titles

    def objective(self):
        return ExerciseObjective(
            title=self.title_input.text().strip(),
            description=self.description_input.toPlainText().strip(),
            supporting_injects=self.selected_inject_numbers(),
            supporting_doctrine=self.selected_doctrine_titles(),
        )