from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
)


class ObjectivesPanel(QGroupBox):
    """
    Displays the exercise objectives.

    This panel presents objective information and notifies the main window
    when the user wants to add a new objective.
    """

    add_objective_requested = Signal()

    def __init__(self):
        super().__init__("Exercise Objectives")

        layout = QVBoxLayout()

        self.summary = QLabel(
            "No exercise objectives have been defined."
        )
        self.summary.setWordWrap(True)
        layout.addWidget(self.summary)

        self.objectives_list = QListWidget()
        layout.addWidget(self.objectives_list)

        self.add_objective_button = QPushButton("Add Objective")
        self.add_objective_button.clicked.connect(
            self.add_objective_requested.emit
        )
        layout.addWidget(self.add_objective_button)

        self.setLayout(layout)

    def set_objectives(self, objectives):
        self.objectives_list.clear()

        if not objectives:
            self.summary.setText(
                "No exercise objectives have been defined."
            )
            return

        self.summary.setText(
            f"{len(objectives)} exercise objectives defined."
        )

        for number, objective in enumerate(objectives, start=1):
            title = objective.title.strip() or "Untitled objective"

            self.objectives_list.addItem(
                f"{number}. {title}"
            )

    def clear(self):
        self.summary.setText(
            "No exercise objectives have been defined."
        )
        self.objectives_list.clear()