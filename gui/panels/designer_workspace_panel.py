from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class DesignerWorkspacePanel(QWidget):
    """
    Read-only designer workspace.

    Presents the relationship between exercise objectives,
    success criteria and supporting MEL/MIL activity without
    requiring the designer to understand the underlying
    project data model.
    """

    open_in_workspace_requested = Signal(int)

    def __init__(self):
        super().__init__()

        self.project = None
        self.selected_objective = None

        main_layout = QVBoxLayout(self)

        heading = QLabel("Designer Workspace")
        heading.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )
        main_layout.addWidget(heading)

        self.journey_label = QLabel(
            "PREPARE  →  RUN  →  UNDERSTAND  →  DECIDE"
        )
        self.journey_label.setStyleSheet(
            "font-size: 13px; font-weight: bold;"
        )
        main_layout.addWidget(self.journey_label)

        question = QLabel(
            "What are we trying to achieve?"
        )
        question.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        main_layout.addWidget(question)

        content = QHBoxLayout()
        main_layout.addLayout(content, 1)

        objectives_group = QGroupBox(
            "Exercise Objectives"
        )
        objectives_layout = QVBoxLayout(
            objectives_group
        )

        self.objectives_summary = QLabel(
            "No exercise objectives have been defined."
        )
        self.objectives_summary.setWordWrap(True)
        objectives_layout.addWidget(
            self.objectives_summary
        )

        self.objectives_list = QListWidget()
        self.objectives_list.currentRowChanged.connect(
            self._objective_selected
        )
        objectives_layout.addWidget(
            self.objectives_list,
            1,
        )

        content.addWidget(objectives_group, 2)

        design_group = QGroupBox("Design Chain")
        design_layout = QVBoxLayout(design_group)

        self.design_chain = QLabel(
            "Select an objective to review its design chain."
        )
        self.design_chain.setWordWrap(True)
        self.design_chain.setAlignment(
            self.design_chain.alignment()
        )
        design_layout.addWidget(
            self.design_chain,
            1,
        )

        self.open_button = QPushButton(
            "Open Supporting Activity"
        )
        self.open_button.setEnabled(False)
        self.open_button.clicked.connect(
            self._open_supporting_activity
        )
        design_layout.addWidget(self.open_button)

        content.addWidget(design_group, 3)

    def set_project(self, project):
        """
        Display the current project's objective design picture.
        """

        self.project = project
        self.selected_objective = None

        self.objectives_list.clear()
        self.open_button.setEnabled(False)

        if project is None or not project.objectives:
            self.objectives_summary.setText(
                "No exercise objectives have been defined."
            )
            self.design_chain.setText(
                "Add an exercise objective to begin "
                "building the design chain."
            )
            return

        self.objectives_summary.setText(
            f"{len(project.objectives)} exercise objectives defined."
        )

        for number, objective in enumerate(
            project.objectives,
            start=1,
        ):
            title = (
                objective.title.strip()
                or "Untitled objective"
            )

            item = QListWidgetItem(
                f"{number}. {title}"
            )
            self.objectives_list.addItem(item)

        self.objectives_list.setCurrentRow(0)

    def _objective_selected(self, row):
        if (
            self.project is None
            or row < 0
            or row >= len(self.project.objectives)
        ):
            self.selected_objective = None
            self.design_chain.setText(
                "Select an objective to review "
                "its design chain."
            )
            self.open_button.setEnabled(False)
            return

        objective = self.project.objectives[row]
        self.selected_objective = objective

        success_criteria = getattr(
            objective,
            "success_criteria",
            [],
        )

        supporting_injects = getattr(
            objective,
            "supporting_injects",
            [],
        )

        if success_criteria:
            criteria_text = "\n".join(
                f"• {criterion}"
                for criterion in success_criteria
            )
        else:
            criteria_text = (
                "No success criteria currently defined."
            )

        inject_lines = []

        for inject_number in supporting_injects:
            inject = self._find_inject(
                inject_number
            )

            if inject is None:
                inject_lines.append(
                    f"• Inject {inject_number}"
                )
                continue

            exercise_time = (
                inject.exercise_time.strip()
                if inject.exercise_time
                else "Time not set"
            )

            title = (
                inject.title.strip()
                or "Untitled activity"
            )

            inject_lines.append(
                f"• Inject {inject_number} — "
                f"{exercise_time} — {title}"
            )

        if inject_lines:
            inject_text = "\n".join(inject_lines)
        else:
            inject_text = (
                "No supporting MEL/MIL activity "
                "currently identified."
            )

        doctrine = getattr(
            objective,
            "supporting_doctrine",
            [],
        )

        if doctrine:
            doctrine_text = "\n".join(
                f"• {reference}"
                for reference in doctrine
            )
        else:
            doctrine_text = (
                "No supporting doctrine currently linked."
            )

        self.design_chain.setText(
            f"WHY?\n"
            f"{objective.title}\n\n"
            f"WHAT MUST THEY DEMONSTRATE?\n"
            f"{criteria_text}\n\n"
            f"HOW WILL WE CREATE THE OPPORTUNITY?\n"
            f"{inject_text}\n\n"
            f"WHAT SUPPORTS THE DESIGN?\n"
            f"{doctrine_text}"
        )

        self.open_button.setEnabled(
            bool(supporting_injects)
        )

    def _find_inject(self, inject_number):
        if self.project is None:
            return None

        for inject in self.project.injects:
            if inject.number == inject_number:
                return inject

        return None

    def _open_supporting_activity(self):
        if self.selected_objective is None:
            return

        supporting_injects = getattr(
            self.selected_objective,
            "supporting_injects",
            [],
        )

        if not supporting_injects:
            return

        self.open_in_workspace_requested.emit(
            supporting_injects[0]
        )