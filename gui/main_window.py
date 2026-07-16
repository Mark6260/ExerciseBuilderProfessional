from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from core.assurance import ExerciseAssurance
from core.project import Project
from core.word_parser import WordParser
from gui.dialogs.objective_dialog import ObjectiveDialog
from gui.panels.assurance_panel import AssurancePanel
from gui.panels.inject_details_panel import InjectDetailsPanel
from gui.panels.master_events_list_panel import MasterEventsListPanel
from gui.panels.objectives_panel import ObjectivesPanel
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

        self.import_word_action = QAction(
            "Exercise Pack from Word...",
            self,
        )
        import_menu.addAction(self.import_word_action)

        self.new_action.triggered.connect(self.new_project)
        self.open_action.triggered.connect(self.open_project)
        self.save_action.triggered.connect(self.save_project)
        self.save_as_action.triggered.connect(self.save_project_as)
        self.exit_action.triggered.connect(self.close)
        self.import_word_action.triggered.connect(
            self.import_word_document
        )

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
        self.objectives_panel = ObjectivesPanel()
        self.mel_panel = MasterEventsListPanel()
        self.inject_details_panel = InjectDetailsPanel()
        self.assurance_panel = AssurancePanel()

        self.mel_panel.inject_selected.connect(
            self.show_inject_details
        )

        self.objectives_panel.add_objective_requested.connect(
            self.add_objective
        )

        self.assurance_panel.open_workspace_requested.connect(
            lambda: self.tabs.setCurrentIndex(1)
        )

        workspace = QWidget()
        workspace_layout = QHBoxLayout(workspace)

        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)

        left_layout.addWidget(self.project_panel, 1)
        left_layout.addWidget(self.objectives_panel, 2)

        workspace_layout.addWidget(left_column, 2)
        workspace_layout.addWidget(self.mel_panel, 3)
        workspace_layout.addWidget(self.inject_details_panel, 6)

        self.tabs = QTabWidget()

        self.tabs.addTab(
            self.assurance_panel,
            "Exercise Assurance",
        )

        self.tabs.addTab(
            workspace,
            "Exercise Workspace",
        )

        self.setCentralWidget(self.tabs)

    def update_project_view(self):
        self.project_panel.update_project(
            name=self.current_project.name,
            filename=self.current_file,
        )

        self.objectives_panel.set_objectives(
            self.current_project.objectives
        )

        self.mel_panel.set_injects(
            self.current_project.injects
        )

        if self.current_project.injects:
            self.mel_panel.list_widget.setCurrentRow(0)
        else:
            self.clear_inject_details()

        self.update_assurance()

        self.setWindowTitle(
            f"Exercise Director — {self.current_project.name}"
        )

        self.tabs.setCurrentIndex(0)

    def update_assurance(self):
        assurance = ExerciseAssurance(self.current_project)
        results = assurance.check()

        self.assurance_panel.show_results(results)

    def add_objective(self):
        dialog = ObjectiveDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        objective = dialog.objective()
        self.current_project.add_objective(objective)

        self.objectives_panel.set_objectives(
            self.current_project.objectives
        )
        self.update_assurance()

        self.statusBar().showMessage(
            f"Objective added: {objective.title}"
        )

    def clear_inject_details(self):
        panel = self.inject_details_panel

        panel.title.setText("No inject selected")
        panel.due.setText("Due: -")

        panel.phase.setText("-")
        panel.category.setText("-")
        panel.source.setText("-")
        panel.method.setText("-")
        panel.audience.setText("-")

        panel.content.clear()
        panel.expected.clear()
        panel.notes.clear()
        panel.attachments.setText("None")

    def show_inject_details(self, row):
        if row < 0 or row >= len(self.current_project.injects):
            self.clear_inject_details()
            return

        inject = self.current_project.injects[row]
        panel = self.inject_details_panel

        panel.title.setText(
            inject.title or f"Inject {inject.number}"
        )
        panel.due.setText(
            f"Due: {inject.exercise_time or '-'}"
        )

        panel.phase.setText(inject.phase or "-")
        panel.category.setText(inject.category or "-")
        panel.source.setText(inject.source or "-")
        panel.method.setText(inject.method or "-")
        panel.audience.setText(inject.audience or "-")

        panel.content.setPlainText(inject.inject_text or "")
        panel.expected.setPlainText(
            inject.expected_action or ""
        )
        panel.notes.setPlainText(
            inject.facilitator_notes or ""
        )

        if inject.attachments:
            attachment_text = "\n".join(
                f"• {attachment}"
                for attachment in inject.attachments
            )
        else:
            attachment_text = "None"

        panel.attachments.setText(attachment_text)

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
            self.current_project.name = self._suggest_project_name(
                filename
            )
            self.current_file = None

            self.update_project_view()

            self.statusBar().showMessage(
                f"Imported {len(self.current_project.injects)} injects"
            )

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