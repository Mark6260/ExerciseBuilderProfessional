from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QLabel,
    QGroupBox,
    QFormLayout,
    QStatusBar,
    QToolBar,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtGui import QAction

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
        self.update_project_view()

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready")

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
        form = QFormLayout()

        self.project_name = QLabel()
        self.project_author = QLabel()
        self.project_location = QLabel()

        form.addRow("Name:", self.project_name)
        form.addRow("Author:", self.project_author)
        form.addRow("Folder:", self.project_location)

        project_group.setLayout(form)

        exercise_group = QGroupBox("Exercises")
        self.exercise_list = QListWidget()

        layout_right = QVBoxLayout()
        layout_right.addWidget(self.exercise_list)
        exercise_group.setLayout(layout_right)

        main_layout = QHBoxLayout()
        main_layout.addWidget(project_group, 1)
        main_layout.addWidget(exercise_group, 3)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def update_project_view(self):
        self.project_name.setText(self.current_project.name)
        self.project_author.setText("-")
        self.project_location.setText(self.current_file or "-")

        self.exercise_list.clear()
        for exercise in self.current_project.exercises:
            self.exercise_list.addItem(str(exercise))

        self.setWindowTitle(f"ExerciseBuilder Professional - {self.current_project.name}")

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
            "ExerciseBuilder Project (*.json)"
        )

        if not filename:
            return

        try:
            self.current_project = Project.load(filename)
            self.current_file = filename
            self.update_project_view()
            self.statusBar().showMessage("Project opened")
        except Exception as error:
            QMessageBox.critical(self, "Open Project Error", str(error))

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
            "ExerciseBuilder Project (*.json)"
        )

        if not filename:
            return

        if not filename.endswith(".json"):
            filename += ".json"

        self.current_file = filename
        self._save_to_file(filename)

    def _save_to_file(self, filename):
        try:
            self.current_project.save(filename)
            self.current_file = filename
            self.update_project_view()
            self.statusBar().showMessage("Project saved")
        except Exception as error:
            QMessageBox.critical(self, "Save Project Error", str(error))

    def import_word_document(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Word Document",
            "",
            "Word Documents (*.docx)"
        )

        if not filename:
            return

        try:
            parser = WordParser(filename)
            parser.open()

            info = parser.get_summary()

            QMessageBox.information(
    self,
    "Document Information",
    f"Paragraphs: {info['paragraphs']}\n"
    f"Tables: {info['tables']}\n"
    f"Injects Found: {info['injects']}"
)

        except Exception as error:
            QMessageBox.critical(
                self,
                "Import Error",
                str(error)
            )