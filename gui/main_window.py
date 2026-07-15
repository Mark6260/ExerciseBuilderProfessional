from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QScrollArea,
    QStatusBar,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from core.project import Project
from core.word_parser import WordParser
from gui.panels.master_events_list_panel import MasterEventsListPanel
from gui.panels.project_panel import ProjectPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_project = Project()
        self.current_file = None

        self.setWindowTitle("Exercise Director")
        self.resize(1400, 820)

        self.create_menu()
        self.create_toolbar()
        self.create_layout()

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready")

        self.update_project_view()

    def create_menu(self):
        file_menu = self.menuBar().addMenu("File")

        self.new_action = QAction("New Project", self)
        self.open_action = QAction("Open Project", self)
        self.save_action = QAction("Save Project", self)
        self.save_as_action = QAction("Save Project As", self)
        self.exit_action = QAction("Exit", self)

        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        import_menu = self.menuBar().addMenu("Import")
        self.import_word_action = QAction("Exercise Pack from Word...", self)
        import_menu.addAction(self.import_word_action)

        self.new_action.triggered.connect(self.new_project)
        self.open_action.triggered.connect(self.open_project)
        self.save_action.triggered.connect(self.save_project)
        self.save_as_action.triggered.connect(self.save_project_as)
        self.exit_action.triggered.connect(self.close)
        self.import_word_action.triggered.connect(self.import_word_document)

    def create_toolbar(self):
        toolbar = QToolBar("Main")
        toolbar.setMovable(False)

        self.addToolBar(toolbar)

        toolbar.addAction(self.new_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()
        toolbar.addAction(self.import_word_action)

    def create_layout(self):
        self.project_panel = ProjectPanel()

        self.mel_panel = MasterEventsListPanel()
        self.mel_panel.inject_selected.connect(self.show_inject_details)

        inject_details_panel = self.create_inject_details_panel()

        layout = QHBoxLayout()
        layout.addWidget(self.project_panel, 1)
        layout.addWidget(self.mel_panel, 2)
        layout.addWidget(inject_details_panel, 4)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_inject_details_panel(self):
        group = QGroupBox("Inject Details")

        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)

        self.detail_title = QLabel("No inject selected")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self.detail_title.setFont(title_font)
        self.detail_title.setWordWrap(True)

        self.detail_due = QLabel("Due: -")

        layout.addWidget(self.detail_title)
        layout.addWidget(self.detail_due)

        overview_group = QGroupBox("Overview")
        overview_form = QFormLayout()

        self.detail_phase = QLabel("-")
        self.detail_category = QLabel("-")
        self.detail_source = QLabel("-")
        self.detail_method = QLabel("-")
        self.detail_audience = QLabel("-")

        overview_form.addRow("Phase:", self.detail_phase)
        overview_form.addRow("Category:", self.detail_category)
        overview_form.addRow("Source:", self.detail_source)
        overview_form.addRow("Method:", self.detail_method)
        overview_form.addRow("Audience:", self.detail_audience)

        overview_group.setLayout(overview_form)
        layout.addWidget(overview_group)

        self.detail_content = self.create_text_section(
            layout,
            "Content",
            180,
        )
        self.detail_expected_action = self.create_text_section(
            layout,
            "Expected Action",
            110,
        )
        self.detail_facilitator_notes = self.create_text_section(
            layout,
            "Facilitator Notes",
            110,
        )

        layout.addWidget(self.create_heading("Attachments"))

        self.detail_attachments = QLabel("None")
        self.detail_attachments.setWordWrap(True)
        self.detail_attachments.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        layout.addWidget(self.detail_attachments)
        layout.addStretch()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)

        group_layout = QVBoxLayout()
        group_layout.addWidget(scroll_area)
        group.setLayout(group_layout)

        return group

    def create_text_section(self, layout, heading, minimum_height):
        layout.addWidget(self.create_heading(heading))

        text_box = QTextEdit()
        text_box.setReadOnly(True)
        text_box.setMinimumHeight(minimum_height)

        layout.addWidget(text_box)

        return text_box

    @staticmethod
    def create_heading(text):
        label = QLabel(text)

        font = QFont()
        font.setPointSize(11)
        font.setBold(True)

        label.setFont(font)
        return label

    def update_project_view(self):
        self.project_panel.update_project(
            name=self.current_project.name,
            filename=self.current_file,
        )

        self.mel_panel.set_injects(self.current_project.injects)

        if self.current_project.injects:
            self.mel_panel.list_widget.setCurrentRow(0)
        else:
            self.clear_inject_details()

        self.setWindowTitle(
            f"Exercise Director — {self.current_project.name}"
        )

    def clear_inject_details(self):
        self.detail_title.setText("No inject selected")
        self.detail_due.setText("Due: -")
        self.detail_phase.setText("-")
        self.detail_category.setText("-")
        self.detail_source.setText("-")
        self.detail_method.setText("-")
        self.detail_audience.setText("-")
        self.detail_content.clear()
        self.detail_expected_action.clear()
        self.detail_facilitator_notes.clear()
        self.detail_attachments.setText("None")

    def show_inject_details(self, row):
        if row < 0 or row >= len(self.current_project.injects):
            self.clear_inject_details()
            return

        inject = self.current_project.injects[row]

        self.detail_title.setText(
            inject.title or f"Inject {inject.number}"
        )
        self.detail_due.setText(
            f"Due: {inject.exercise_time or '-'}"
        )
        self.detail_phase.setText(inject.phase or "-")
        self.detail_category.setText(inject.category or "-")
        self.detail_source.setText(inject.source or "-")
        self.detail_method.setText(inject.method or "-")
        self.detail_audience.setText(inject.audience or "-")
        self.detail_content.setPlainText(inject.inject_text or "")
        self.detail_expected_action.setPlainText(
            inject.expected_action or ""
        )
        self.detail_facilitator_notes.setPlainText(
            inject.facilitator_notes or ""
        )

        attachments = (
            "\n".join(f"• {item}" for item in inject.attachments)
            if inject.attachments
            else "None"
        )
        self.detail_attachments.setText(attachments)

    def new_project(self):
        self.current_project = Project()
        self.current_file = None
        self.update_project_view()
        self.statusBar().showMessage("New project created")

    def open_project(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Project",
            "",
            "Exercise Director Project (*.json)",
        )

        if not filename:
            return

        try:
            self.current_project = Project.load(filename)
            self.current_file = filename
            self.update_project_view()
            self.statusBar().showMessage("Project opened")
        except Exception as error:
            QMessageBox.critical(
                self,
                "Open Project Error",
                str(error),
            )

    def save_project(self):
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self.save_project_as()

    def save_project_as(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project",
            "",
            "Exercise Director Project (*.json)",
        )

        if not filename:
            return

        if not filename.lower().endswith(".json"):
            filename += ".json"

        self._save_to_file(filename)

    def _save_to_file(self, filename):
        try:
            self.current_project.save(filename)
            self.current_file = filename
            self.update_project_view()
            self.statusBar().showMessage("Project saved")
        except Exception as error:
            QMessageBox.critical(
                self,
                "Save Project Error",
                str(error),
            )

    def import_word_document(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Import Exercise Pack",
            "",
            "Word Documents (*.docx)",
        )

        if not filename:
            return

        try:
            parser = WordParser(filename)
            parser.open()

            self.current_project.injects = parser.get_injects()
            self.current_project.name = self._suggest_project_name(filename)
            self.current_file = None

            self.update_project_view()

            QMessageBox.information(
                self,
                "Import Complete",
                f"Imported {len(self.current_project.injects)} injects.",
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Import Error",
                str(error),
            )

    @staticmethod
    def _suggest_project_name(filename):
        filename = filename.replace("\\", "/")
        name = filename.rsplit("/", 1)[-1]

        if name.lower().endswith(".docx"):
            name = name[:-5]

        return name.replace("_", " ").strip()