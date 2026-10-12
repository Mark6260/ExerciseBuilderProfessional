from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
class PresentationPanel(QWidget):
    """Workspace for managing exercise presentations."""

    save_requested = Signal()


    def __init__(self, parent=None):
        super().__init__(parent)

        self.project = None

        layout = QVBoxLayout(self)

        heading = QLabel("EXERCISE PRESENTATIONS")
        heading.setStyleSheet(
            "font-size: 20px; "
            "font-weight: bold;"
        )

        introduction = QLabel(
            "Manage PowerPoint presentations associated "
            "with this exercise."
        )
        introduction.setWordWrap(True)

        self.project_label = QLabel(
            "No exercise project loaded."
        )
        self.attach_button = QPushButton(
            "Attach PowerPoint..."
        )
        self.attach_button.setEnabled(False)
        self.attach_button.clicked.connect(self.select_presentation)

        self.presentation_list = QListWidget()
        self.presentation_list.setMinimumHeight(180)

        layout.addWidget(heading)
        layout.addWidget(introduction)
        layout.addWidget(self.project_label)
        layout.addWidget(self.attach_button)
        layout.addWidget(self.presentation_list)
        layout.addStretch()

    def set_project(self, project):
        self.project = project

        if project is None:
            self.project_label.setText(
                "No exercise project loaded."
            )
        else:
            self.project_label.setText(
                f"Exercise: {project.name}"
            )

        self.refresh_presentation_list()

    def refresh_presentation_list(self):
        """Display presentations registered with the exercise."""

        self.presentation_list.clear()

        if self.project is None:
            return

        for asset in self.project.presentation_assets:
            self.presentation_list.addItem(
                asset.get("filename", "Unnamed Presentation")
            )

    def set_project_filename(self, filename):
        self.project_filename = filename
        self.attach_button.setEnabled(
            self.project is not None and bool(filename)
        )
    def select_presentation(self):
        """Allow the user to select a PowerPoint file."""

        if self.project is None or not self.project_filename:
            return

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Exercise PowerPoint",
            "",
            "PowerPoint Presentations (*.pptx)",
        )

        if not filename:
            return

        try:
            asset = self.project.register_presentation(
                self.project_filename,
                filename,
            )

        except FileExistsError:
            QMessageBox.warning(
                self,
                "Presentation Already Attached",
                "A presentation with this filename already "
                "exists in the exercise folder.\n\n"
                "The existing presentation has not been changed.",
            )
            return

        except Exception as error:
            QMessageBox.critical(
                self,
                "PowerPoint Import Error",
                str(error),
            )
            return

        print(
            f"Registered PowerPoint: {asset['relative_path']}"
        )

        self.save_requested.emit()
        self.refresh_presentation_list()