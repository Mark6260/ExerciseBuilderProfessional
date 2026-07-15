from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLabel,
)


class ProjectPanel(QGroupBox):
    def __init__(self):
        super().__init__("Project")

        self.name_label = QLabel("-")
        self.author_label = QLabel("-")
        self.file_label = QLabel("-")

        self.name_label.setWordWrap(True)
        self.author_label.setWordWrap(True)
        self.file_label.setWordWrap(True)

        layout = QFormLayout()
        layout.addRow("Name:", self.name_label)
        layout.addRow("Author:", self.author_label)
        layout.addRow("File:", self.file_label)

        self.setLayout(layout)

    def update_project(
        self,
        name: str,
        author: str = "-",
        filename: str | None = None,
    ):
        self.name_label.setText(name or "Untitled Project")
        self.author_label.setText(author or "-")
        self.file_label.setText(filename or "-")