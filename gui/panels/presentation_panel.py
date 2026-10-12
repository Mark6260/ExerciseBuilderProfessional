from PySide6.QtCore import QEvent, Qt, Signal
import os
from PySide6.QtGui import QPixmap
from pathlib import Path
from pptx import Presentation
from core.presentation_renderer import render_presentation
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
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
        self.current_slide_pixmap = None

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
        self.slide_count_label = QLabel(
            "Slides: Select a PowerPoint to view details"
        )
        self.slide_list = QListWidget()
        self.slide_list.setMinimumHeight(180)
        self.slide_list.setEnabled(False)
        self.slide_list.itemSelectionChanged.connect(
            self.update_slide_preview
        )
        self.slide_preview_label = QLabel(
            "Select a slide to preview"
        )
        self.slide_preview_label.installEventFilter(self)
        self.slide_preview_label.setMinimumHeight(200)
        self.slide_preview_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.slide_preview_label.setStyleSheet(
            "QLabel {"
            "background-color: #202832;"
            "color: white;"
            "border: 1px solid #526070;"
            "border-radius: 6px;"
            "}"
        )
        self.open_button = QPushButton("Open Selected PowerPoint")
        self.open_button.setEnabled(False)
        self.generate_previews_button = QPushButton(
            "Generate Slide Previews"
        )
        self.generate_previews_button.setEnabled(False)
        self.generate_previews_button.clicked.connect(
            self.generate_slide_previews
        )
        self.open_button.clicked.connect(
            self.open_selected_presentation
        )
        self.presentation_list.itemSelectionChanged.connect(
            self.update_open_button
        )

        layout.addWidget(heading)
        layout.addWidget(introduction)
        layout.addWidget(self.project_label)
        layout.addWidget(self.attach_button)
        layout.addWidget(self.presentation_list)
        layout.addWidget(self.slide_count_label)
        slide_workspace = QHBoxLayout()

        slide_workspace.addWidget(
            self.slide_list,
            1,
        )

        slide_workspace.addWidget(
            self.slide_preview_label,
            3,
        )

        layout.addLayout(slide_workspace)
        layout.addWidget(self.open_button)
        layout.addWidget(self.generate_previews_button)
        layout.addStretch()
        
    def display_slide_image(self, image_path):
        """Display a rendered PowerPoint slide in the preview area."""

        pixmap = QPixmap(str(image_path))

        if pixmap.isNull():
            self.slide_preview_label.setText(
                "Unable to display slide image"
            )
            return
        
        self.current_slide_pixmap = pixmap
        preview_size = self.slide_preview_label.size()

        scaled_pixmap = pixmap.scaled(
            preview_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.slide_preview_label.setPixmap(scaled_pixmap)
        
    def resize_slide_preview(self):
        """Resize the displayed slide without distortion."""

        if self.current_slide_pixmap is None:
            return

        preview_size = self.slide_preview_label.size()

        if preview_size.width() <= 0 or preview_size.height() <= 0:
            return

        scaled_pixmap = self.current_slide_pixmap.scaled(
            preview_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.slide_preview_label.setPixmap(scaled_pixmap)
        
    def eventFilter(self, watched, event):
        """Update the slide image when the preview area resizes."""

        if (
            watched is self.slide_preview_label
            and event.type() == QEvent.Type.Resize
        ):
            self.resize_slide_preview()

        return super().eventFilter(watched, event)
      
    def open_selected_presentation(self):
        """Identify the PowerPoint selected by the user."""

        if self.project is None:
            return

        selected_row = self.presentation_list.currentRow()

        if selected_row < 0:
            return

        assets = self.project.presentation_assets

        if selected_row >= len(assets):
            return

        asset = assets[selected_row]

        presentation_path = (
            Path(self.project_filename).resolve().parent
            / asset["relative_path"]
        )

        if not presentation_path.is_file():
            QMessageBox.warning(
                self,
                "PowerPoint Not Found",
                f"The presentation could not be found:\n\n"
                f"{presentation_path}",
            )
            return

        try:
            os.startfile(str(presentation_path))
        except OSError as error:
            QMessageBox.critical(
                self,
                "Cannot Open PowerPoint",
                str(error),
            )

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
    def update_open_button(self):
        """Enable opening when a presentation is selected."""

        has_selection = (
            self.presentation_list.currentItem() is not None
        )

        self.open_button.setEnabled(
            self.project is not None
            and has_selection
        )
        self.generate_previews_button.setEnabled(
            self.project is not None
            and bool(self.project_filename)
            and has_selection
        )
        self.update_slide_count()
        
    def update_slide_count(self):
        """Display the number of slides in the selected PowerPoint."""

        self.slide_list.clear()
        self.slide_list.setEnabled(False)
        self.slide_count_label.setText(
            "Slides: Select a PowerPoint to view details"
        )

        if self.project is None or not self.project_filename:
            return

        selected_row = self.presentation_list.currentRow()
        assets = self.project.presentation_assets

        if selected_row < 0 or selected_row >= len(assets):
            return

        presentation_path = (
            Path(self.project_filename).resolve().parent
            / assets[selected_row]["relative_path"]
        )

        if not presentation_path.is_file():
            self.slide_count_label.setText("Slides: File not found")
            return

        try:
            presentation = Presentation(str(presentation_path))
            count = len(presentation.slides)
            self.slide_count_label.setText(f"Slides: {count}")
            for number in range(1, count + 1):
                self.slide_list.addItem(f"Slide {number}")

            self.slide_list.setEnabled(True)
        except Exception:
            self.slide_count_label.setText(
                "Slides: Unable to read presentation"
            )
    def update_slide_preview(self):
        self.current_slide_pixmap = None
        """Identify the slide selected for preview."""

        selected_row = self.slide_list.currentRow()

        if selected_row < 0:
            self.slide_preview_label.setText(
                "Select a slide to preview"
            )
            return

        slide_number = selected_row + 1

        if self.project is None or not self.project_filename:
            return

        presentation_row = self.presentation_list.currentRow()
        assets = self.project.presentation_assets

        if presentation_row < 0 or presentation_row >= len(assets):
            return

        asset = assets[presentation_row]

        project_folder = Path(self.project_filename).resolve().parent

        preview_image = (
            project_folder
            / "assets"
            / "previews"
            / asset["id"]
            / f"slide_{slide_number:03d}.png"
        )
        self.current_slide_pixmap = None
        self.slide_preview_label.clear()

        if preview_image.is_file():
            self.display_slide_image(preview_image)
        else:
            self.slide_preview_label.setText(
                f"Slide {slide_number}\n\n"
                "Preview not generated yet"
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
    def generate_slide_previews(self):
        """Identify the presentation and its preview destination."""

        if self.project is None or not self.project_filename:
            return

        selected_row = self.presentation_list.currentRow()
        assets = self.project.presentation_assets

        if selected_row < 0 or selected_row >= len(assets):
            return

        asset = assets[selected_row]

        project_folder = Path(self.project_filename).resolve().parent

        source_path = (
            project_folder / asset["relative_path"]
        )

        preview_folder = (
            project_folder
            / "assets"
            / "previews"
            / asset["id"]
        )

        if not source_path.is_file():
            QMessageBox.warning(
                self,
                "PowerPoint Not Found",
                f"Cannot find the presentation:\n\n{source_path}",
            )
            return

        try:
            slide_count = render_presentation(
                source_path,
                preview_folder,
            )

        except FileExistsError:
            QMessageBox.warning(
                self,
                "Previews Already Exist",
                "This presentation already has a preview folder "
                "containing files.\n\n"
                "Existing previews have not been overwritten.",
            )
            return

        except Exception as error:
            QMessageBox.critical(
                self,
                "Preview Generation Failed",
                str(error),
            )
            return

        QMessageBox.information(
            self,
            "Slide Previews Generated",
            f"Successfully generated {slide_count} slide previews.",
        )