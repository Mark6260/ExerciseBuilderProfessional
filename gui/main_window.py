from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
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
        project_panel = self.create_project_panel()
        inject_list_panel = self.create_inject_list_panel()
        current_inject_panel = self.create_current_inject_panel()

        main_layout = QHBoxLayout()
        main_layout.addWidget(project_panel, 1)
        main_layout.addWidget(inject_list_panel, 2)
        main_layout.addWidget(current_inject_panel, 4)

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

    def create_project_panel(self):
        project_group = QGroupBox("Project")
        project_form = QFormLayout()

        self.project_name = QLabel("-")
        self.project_author = QLabel("-")
        self.project_location = QLabel("-")

        self.project_name.setWordWrap(True)
        self.project_location.setWordWrap(True)

        project_form.addRow("Name:", self.project_name)
        project_form.addRow("Author:", self.project_author)
        project_form.addRow("File:", self.project_location)

        project_group.setLayout(project_form)

        return project_group

    def create_inject_list_panel(self):
        inject_group = QGroupBox("Injects")
        inject_layout = QVBoxLayout()

        self.inject_list = QListWidget()
        self.inject_list.currentRowChanged.connect(
            self.show_inject_details
        )

        inject_layout.addWidget(self.inject_list)
        inject_group.setLayout(inject_layout)

        return inject_group

    def create_current_inject_panel(self):
        current_inject_group = QGroupBox("Current Inject")

        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_widget.setLayout(content_layout)

        self.detail_title = QLabel("No inject selected")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self.detail_title.setFont(title_font)
        self.detail_title.setWordWrap(True)

        self.detail_due = QLabel("Due: -")
        due_font = QFont()
        due_font.setPointSize(12)
        due_font.setBold(True)
        self.detail_due.setFont(due_font)

        content_layout.addWidget(self.detail_title)
        content_layout.addWidget(self.detail_due)

        metadata_group = QGroupBox("Overview")
        metadata_form = QFormLayout()

        self.detail_phase = QLabel("-")
        self.detail_category = QLabel("-")
        self.detail_source = QLabel("-")
        self.detail_method = QLabel("-")
        self.detail_audience = QLabel("-")

        self.detail_phase.setWordWrap(True)
        self.detail_category.setWordWrap(True)
        self.detail_source.setWordWrap(True)
        self.detail_method.setWordWrap(True)
        self.detail_audience.setWordWrap(True)

        metadata_form.addRow("Phase:", self.detail_phase)
        metadata_form.addRow("Category:", self.detail_category)
        metadata_form.addRow("Source:", self.detail_source)
        metadata_form.addRow("Method:", self.detail_method)
        metadata_form.addRow("Audience:", self.detail_audience)

        metadata_group.setLayout(metadata_form)
        content_layout.addWidget(metadata_group)

        content_layout.addWidget(self.create_section_heading("Content"))

        self.detail_content = QTextEdit()
        self.detail_content.setReadOnly(True)
        self.detail_content.setPlaceholderText(
            "The inject content will appear here."
        )
        self.detail_content.setMinimumHeight(180)

        content_layout.addWidget(self.detail_content)

        content_layout.addWidget(
            self.create_section_heading("Expected Action")
        )

        self.detail_expected_action = QTextEdit()
        self.detail_expected_action.setReadOnly(True)
        self.detail_expected_action.setPlaceholderText(
            "The expected action will appear here."
        )
        self.detail_expected_action.setMinimumHeight(110)

        content_layout.addWidget(self.detail_expected_action)

        content_layout.addWidget(
            self.create_section_heading("Facilitator Notes")
        )

        self.detail_facilitator_notes = QTextEdit()
        self.detail_facilitator_notes.setReadOnly(True)
        self.detail_facilitator_notes.setPlaceholderText(
            "Facilitator notes will appear here."
        )
        self.detail_facilitator_notes.setMinimumHeight(110)

        content_layout.addWidget(self.detail_facilitator_notes)

        content_layout.addWidget(
            self.create_section_heading("Attachments")
        )

        self.detail_attachments = QLabel("None")
        self.detail_attachments.setWordWrap(True)
        self.detail_attachments.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        content_layout.addWidget(self.detail_attachments)
        content_layout.addStretch()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)

        group_layout = QVBoxLayout()
        group_layout.addWidget(scroll_area)

        current_inject_group.setLayout(group_layout)

        return current_inject_group

    @staticmethod
    def create_section_heading(text):
        heading = QLabel(text)

        font = QFont()
        font.setPointSize(11)
        font.setBold(True)

        heading.setFont(font)

        return heading

    def update_project_view(self):
        self.project_name.setText(self.current_project.name)
        self.project_author.setText("-")
        self.project_location.setText(self.current_file or "-")

        self.inject_list.clear()

        for inject in self.current_project.injects:
            item_text = (
                f"{inject.exercise_time} — {inject.title}"
                if inject.exercise_time
                else str(inject)
            )

            self.inject_list.addItem(item_text)

        if self.inject_list.count() > 0:
            self.inject_list.setCurrentRow(0)
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

        self.detail_content.setPlainText(
            inject.inject_text or ""
        )

        self.detail_expected_action.setPlainText(
            inject.expected_action or ""
        )

        self.detail_facilitator_notes.setPlainText(
            inject.facilitator_notes or ""
        )

        if inject.attachments:
            attachment_text = "\n".join(
                f"• {attachment}"
                for attachment in inject.attachments
            )
        else:
            attachment_text = "None"

        self.detail_attachments.setText(attachment_text)

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

            injects = parser.get_injects()

            self.current_project.injects = injects

            if injects:
                self.current_project.name = (
                    self._suggest_project_name(filename)
                )

            self.current_file = None

            self.update_project_view()

            self.statusBar().showMessage(
                f"Imported {len(injects)} injects"
            )

            QMessageBox.information(
                self,
                "Import Complete",
                f"Imported {len(injects)} injects.",
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