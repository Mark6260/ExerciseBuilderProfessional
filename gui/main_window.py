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
from gui.dialogs.exercise_definition_dialog import (
    ExerciseDefinitionDialog,
)
from core.observation.observer_session import ObserverSession
from gui.dialogs.apprentice_dialog import (
    ApprenticeDialog,
)
from gui.dialogs.objective_dialog import ObjectiveDialog
from gui.panels.assurance_panel import AssurancePanel
from gui.panels.inject_details_panel import InjectDetailsPanel
from gui.panels.master_events_list_panel import MasterEventsListPanel
from gui.panels.apprentice_notebook_panel import (
    ApprenticeNotebookPanel,
)

from gui.panels.objectives_panel import ObjectivesPanel
from gui.panels.project_panel import ProjectPanel
from gui.panels.observer_panel import ObserverPanel
from gui.panels.observation_review_panel import (
    ObservationReviewPanel,
)


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
        self.show_apprentice()
        self.observer_panel = ObserverPanel()

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
        self.save_as_action.triggered.connect(
            self.save_project_as
        )
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
        self.observer_panel = ObserverPanel()
        self.observation_review_panel = ObservationReviewPanel()
        self.observation_review_panel.evidence_admitted.connect(
            self._handle_evidence_admitted
        )
        self.observation_review_panel.set_project(
            self.current_project
        )
        self.observer_panel.observation_recorded.connect(
        self._handle_observation_recorded
    )

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

        workspace_layout.addWidget(left_column, 4)
        workspace_layout.addWidget(self.mel_panel, 4)
        workspace_layout.addWidget(
            self.inject_details_panel,
            7,
        )

        self.tabs = QTabWidget()

        self.tabs.addTab(
            self.assurance_panel,
            "Exercise Assurance",
        )

        self.tabs.addTab(
            workspace,
            "Exercise Workspace",
        )
        self.tabs.addTab(
            self.observer_panel,
            "Observer Mode",
        )

        self.tabs.addTab(
            self.observation_review_panel,
            "Observation Review",
        )
        self.setCentralWidget(self.tabs)

    def _handle_observation_recorded(
        self,
        observation,
    ):
        if self.current_project is None:
            return

        self.current_project.add_observation(
            observation
        )
        self.observation_review_panel.refresh_observations()

        self.statusBar().showMessage(
            "Observation recorded",
            3000,
        )
    def _handle_evidence_admitted(
        self,
        evidence,
    ):
        if self.current_project is None:
            return

        self.current_project.add_evidence(
            evidence
        )

        self.statusBar().showMessage(
            "Observation admitted as evidence",
            3000,
        )

    def update_project_view(self):
        requirement = (
        self.current_project.operational_requirement
    )
    def show_apprentice(self):
        dialog = ApprenticeDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            self.statusBar().showMessage(
            "The Apprentice is standing by"
        )
        return

        self.new_project()


    def update_assurance(self):
        assurance = ExerciseAssurance(
            self.current_project
        )
        results = assurance.check()

        self.assurance_panel.show_results(results)

    def add_objective(self):
        dialog = ObjectiveDialog(
            self.current_project.injects,
            self.current_project.doctrine_references,
            self,
        )

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
        if (
            row < 0
            or row >= len(self.current_project.injects)
        ):
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

        panel.content.setPlainText(
            inject.inject_text or ""
        )

        panel.expected.setPlainText(
            inject.expected_action or ""
        )

        panel.notes.setPlainText(
            inject.facilitator_notes or ""
        )

        if inject.attachments:
            attachment_text = "\n".join(
                f"â€¢ {attachment}"
                for attachment in inject.attachments
            )
        else:
            attachment_text = "None"

            panel.attachments.setText(attachment_text)

    def new_project(self):
        apprentice = ApprenticeDialog(self)

        if apprentice.exec() != QDialog.DialogCode.Accepted:
            self.statusBar().showMessage(
                "The Apprentice is standing by"
            )
            return

        dialog = ExerciseDefinitionDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            self.statusBar().showMessage(
                "Operational readiness analysis cancelled"
            )
            return

        project = Project()

        requirement = project.operational_requirement
        readiness = requirement.readiness

        readiness.required_state = (
            dialog.target_readiness()
        )

        requirement.operational_driver = (
            dialog.operational_requirement()
        )

        readiness.current_state = (
            dialog.current_readiness()
        )

        readiness.required_standard = (
            dialog.required_standard()
        )

        readiness.readiness_gap = (
            dialog.readiness_gap()
        )

        requirement.description = (
            dialog.training_audience()
        )

        requirement.success_criteria = (
            dialog.learning_opportunities()
        )

        self.current_project = project
        self.current_file = None

        self.update_project_view()

        self.statusBar().showMessage(
            "New operational readiness case created"
        )

    def open_project(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Project",
            "",
            "Exercise Director Project (*.json)",
        )

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
            self.statusBar().showMessage(
                "Project opened"
            )

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
            self.statusBar().showMessage(
                "Project saved"
            )

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

            self.current_project.injects = (
                parser.get_injects()
            )

            self.current_project.name = (
                self._suggest_project_name(filename)
            )

            self.current_file = None

            self.update_project_view()

            inject_count = len(
                self.current_project.injects
            )

            self.statusBar().showMessage(
                f"Imported {inject_count} injects"
            )

            QMessageBox.information(
                self,
                "Import Complete",
                f"Imported {inject_count} injects.",
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
