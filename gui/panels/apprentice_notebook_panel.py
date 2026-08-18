from PySide6.QtWidgets import (
    QLabel,
    QGroupBox,
    QVBoxLayout,
)


class ApprenticeNotebookPanel(QGroupBox):

    def __init__(self):
        super().__init__("Apprentice's Notebook")

        self.summary = QLabel()

        self.summary.setWordWrap(True)

        self.summary.setText(
            "○ Mission\n\n"
            "○ Operational Requirement\n\n"
            "○ Training Audience\n\n"
            "○ Current Readiness\n\n"
            "○ Target Readiness\n\n"
            "○ Readiness Gap\n\n"
            "○ Learning Strategy\n\n"
            "○ Evidence"
        )

        layout = QVBoxLayout()

        layout.addWidget(self.summary)

        self.setLayout(layout)

    def update_notebook(self, notebook):

        self.summary.setText(
            notebook.summary()
        )