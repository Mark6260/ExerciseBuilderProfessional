from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QStatusBar,
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

        self.setWindowTitle("ExerciseBuilder Professional")
        self.resize(1200, 750)

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

        self.import_word_action = QAction("Word Document...", self)
        import_menu.addAction(self.import_word_action)

        self.new_action.triggered.connect(self.new_project)
        self.open_action.triggered.connect(self.open_project)
        self.save_action.triggered.connect(self.save_project)
        self.save_as_action.triggered.connect(self.save_project_as)
        self.exit_action.triggered.connect(self.close)
        self.import_word_action.triggered.connect(self.import_word_document)

    def create_toolbar(self):
        toolbar = QToolBar("Main")
        self.addToolBar(toolbar)

        toolbar.addAction(self.new_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)

    def create_layout(self):
        project_group = QGroupBox("Project")
        project_form = QFormLayout()

        self.project_name = QLabel()
        self.project_author = QLabel()
        self.project_location = QLabel()
        self.project_location.setWordWrap(True)

        project_form.addRow("Name:", self.project_name)
        project_form.addRow("Author:", self.project_author)
        project_form.addRow("Folder:", self.project_location)

        project_group.setLayout(project_form)

        inject_group = QGroupBox("Injects")
        inject_layout = QVBoxLayout()

        self.exercise_list = QListWidget()
        self.exercise_list.currentRowChanged.connect(
            self.show_inject_details
        )

        inject_layout.addWidget(self.exercise_list)
        inject_group.setLayout(inject_layout)

        details_group = QGroupBox("Inject Details")
        details_form = QFormLayout()

        self.detail_title = QLabel("-")
        self.detail_time = QLabel("-")
        self.detail_phase = QLabel("-")
        self.detail_category = QLabel("-")

        self.detail_title.setWordWrap(True)
        self.detail_phase.setWordWrap(True)
        self.detail_category.setWordWrap(True)

        details_form.addRow("Title:", self.detail_title)
        details_form.addRow("Exercise Time:", self.detail_time)
        details_form.addRow("Phase:", self.detail_phase)
        details_form.addRow("Category:", self.detail_category)

        details_group.setLayout(details_form)

        main_layout = QHBoxLayout()
        main_layout.addWidget(project_group, 1)
        main_layout.addWidget(inject_group, 2)
        main_layout.addWidget(details_group, 3)

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

    def update_project_view(self):
        self.project_name.setText(self.current_project.name)
        self.project_author.setText("-")
        self.project_location.setText(self.current_file or "-")

        self.exercise_list.clear()

        for inject in self.current_project.exercises:
            self.exercise_list.addItem(str(inject))

        if self.exercise_list.count() > 0:
            self.exercise_list.setCurrentRow(0)
        else:
            self.clear_inject_details()

        self.setWindowTitle(
            f"ExerciseBuilder Professional - {self.current_project.name}"
        )

    def clear_inject_details(self):
        self.detail_title.setText("-")
        self.detail_time.setText("-")
        self.detail_phase.setText("-")
        self.detail_category.setText("-")

    def show_inject_details(self, row):
        if row < 0 or row >= len(self.current_project.exercises):
            self.clear_inject_details()
            return

        inject = self.current_project.exercises[row]

        self.detail_title.setText(
            getattr(inject, "title", "") or "-"
        )
        self.detail_time.setText(
            getattr(inject, "exercise_time", "") or "-"
        )
        self.detail_phase.setText(
            getattr(inject, "phase", "") or "-"
        )
        self.detail_category.setText(
            getattr(inject, "category", "") or "-"
        )

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
            "ExerciseBuilder Project (*.json)",
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
            "ExerciseBuilder Project (*.json)",
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
            "Open Word Document",
            "",
            "Word Documents (*.docx)",
        )

        if not filename:
            return

        try:
            parser = WordParser(filename)
            parser.open()

            injects = parser.get_injects()

            self.current_project.exercises = injects
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