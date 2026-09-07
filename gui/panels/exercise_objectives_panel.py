from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Signal

from core.objective import ExerciseObjective


class ExerciseObjectivesPanel(QWidget):
    """
    Lifecycle workspace for defining the exercise objectives
    that flow from the agreed exercise scope.
    """

    objectives_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.project = None
        self.selected_objective_index = None

        layout = QVBoxLayout(self)

        heading = QLabel(
            "DEFINE EXERCISE OBJECTIVES"
        )
        heading.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        intro = QLabel(
            "Define what the training audience must "
            "demonstrate during the exercise."
        )
        intro.setWordWrap(True)

        self.current_exercise_label = QLabel(
            "Current Exercise: No project loaded"
        )
        self.current_exercise_label.setStyleSheet(
            "font-weight: bold;"
        )

        layout.addWidget(heading)
        layout.addWidget(intro)
        layout.addWidget(
            self.current_exercise_label
        )

        workspace_layout = QHBoxLayout()

        objectives_group = QGroupBox(
            "OBJECTIVES"
        )
        objectives_layout = QVBoxLayout(
            objectives_group
        )

        self.objectives_summary = QLabel(
            "No exercise objectives have been defined."
        )
        self.objectives_summary.setWordWrap(True)

        self.objectives_list = QListWidget()
        self.objectives_list.currentRowChanged.connect(
            self._objective_selected
        )

        self.add_objective_button = QPushButton(
            "Add Objective"
        )
        
        self.add_objective_button.clicked.connect(
            self._start_new_objective
        )

        objectives_layout.addWidget(
            self.objectives_summary
        )
        objectives_layout.addWidget(
            self.objectives_list
        )
        objectives_layout.addWidget(
            self.add_objective_button
        )

        selected_group = QGroupBox(
            "SELECTED OBJECTIVE"
        )
        selected_layout = QVBoxLayout(
            selected_group
        )

        title_label = QLabel("Title")

        self.title_edit = QLineEdit()

        description_label = QLabel(
            "Description"
        )

        self.description_edit = QTextEdit()

        success_criteria_label = QLabel(
            "Success Criteria"
        )

        self.success_criteria_edit = QTextEdit()

        self.save_objective_button = QPushButton(
            "Save Objective"
        )
        self.save_objective_button.clicked.connect(
            self._save_objective
        )

        selected_layout.addWidget(title_label)
        selected_layout.addWidget(
            self.title_edit
        )
        selected_layout.addWidget(
            description_label
        )
        selected_layout.addWidget(
            self.description_edit
        )
        selected_layout.addWidget(
            success_criteria_label
        )
        selected_layout.addWidget(
            self.success_criteria_edit
        )
        selected_layout.addWidget(
            self.save_objective_button
        )

        workspace_layout.addWidget(
            objectives_group,
            1,
        )
        workspace_layout.addWidget(
            selected_group,
            2,
        )

        layout.addLayout(workspace_layout)

    def set_project(self, project):
        """
        Display the objectives owned by the current project.
        """

        self.project = project
        self.objectives_list.clear()

        if project is None:
            self.current_exercise_label.setText(
                "Current Exercise: No project loaded"
            )
            self.objectives_summary.setText(
                "No exercise objectives have been defined."
            )
            return

        self.current_exercise_label.setText(
            f"Current Exercise: {project.name}"
        )

        objectives = project.objectives

        if not objectives:
            self.objectives_summary.setText(
                "No exercise objectives have been defined."
            )
            return

        self.objectives_summary.setText(
            f"{len(objectives)} exercise "
            "objective(s) defined."
        )

        for number, objective in enumerate(
            objectives,
            start=1,
        ):
            title = (
                objective.title
                or "Untitled objective"
            )

            self.objectives_list.addItem(
                f"OBJ {number}: {title}"
            )
            
    def _objective_selected(self, row):
        """
        Display the selected authoritative exercise objective.
        """

        if (
            self.project is None
            or row < 0
            or row >= len(self.project.objectives)
        ):
            return
        self.selected_objective_index = row
        objective = self.project.objectives[row]

        self.title_edit.setText(
            objective.title
        )

        self.description_edit.setPlainText(
            objective.description
        )

        self.success_criteria_edit.setPlainText(
            "\n".join(objective.success_criteria)
        )

    def _start_new_objective(self):
        """
        Prepare the editor for a new exercise objective.
        """
        self.selected_objective_index = None
        
        self.objectives_list.clearSelection()

        self.title_edit.clear()
        self.description_edit.clear()
        self.success_criteria_edit.clear()

        self.title_edit.setFocus()
        
    def _save_objective(self):
        """
        Create a new authoritative exercise objective
        from the editor fields.
        """

        if self.project is None:
            return

        title = self.title_edit.text().strip()

        if not title:
            return

        description = (
            self.description_edit
            .toPlainText()
            .strip()
        )

        success_criteria = [
            line.strip()
            for line in (
                self.success_criteria_edit
                .toPlainText()
                .splitlines()
            )
            if line.strip()
        ]

        if self.selected_objective_index is None:
            objective = ExerciseObjective(
                title=title,
                description=description,
                success_criteria=success_criteria,
            )

            self.project.add_objective(objective)

        else:
            objective = self.project.objectives[
                self.selected_objective_index
            ]

            objective.title = title
            objective.description = description
            objective.success_criteria = success_criteria

        self.set_project(self.project)
        self.objectives_changed.emit()
            