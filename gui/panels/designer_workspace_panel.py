from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QScrollArea,
)
from core.design_assistance import DesignAssistance


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
        self.attention_items = []
        self.selected_attention_item = None

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
        
        self.attention_group = QGroupBox(
            "Needs Your Attention"
        )
        attention_layout = QVBoxLayout(
            self.attention_group
        )

        self.attention_summary = QLabel(
            "No design matters currently require attention."
        )
        self.attention_summary.setWordWrap(True)

        attention_layout.addWidget(
            self.attention_summary
        )

        self.attention_list = QListWidget()
        self.attention_list.currentRowChanged.connect(
            self._attention_selected
        )
        attention_layout.addWidget(
            self.attention_list
        )

        main_layout.addWidget(
            self.attention_group
        )

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
        self.objectives_list.itemClicked.connect(
            self._objective_clicked
        )
        objectives_layout.addWidget(
            self.objectives_list,
            1,
        )

        content.addWidget(objectives_group, 2)
        content.addWidget(objectives_group, 2)

        design_group = QGroupBox("Design Chain")
        design_layout = QVBoxLayout(design_group)

        self.design_chain = QLabel(
            "Select an objective to review its design chain."
        )
        self.design_chain.setWordWrap(True)
        self.design_chain.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.design_chain_scroll = QScrollArea()
        self.design_chain_scroll.setWidgetResizable(True)
        self.design_chain_scroll.setFrameShape(
            QScrollArea.Shape.NoFrame
        )
        self.design_chain_scroll.setWidget(
            self.design_chain
        )

        design_layout.addWidget(
            self.design_chain_scroll,
            1,
        )

        self.open_button = QPushButton(
            "Open Supporting Activity"
        )
        self.open_button.setEnabled(False)
        self.open_button.clicked.connect(
            self._open_supporting_activity
        )

        self.return_to_design_button = QPushButton(
            "Return to Design Chain"
        )
        self.return_to_design_button.setVisible(False)
        self.return_to_design_button.clicked.connect(
            self._return_to_design_chain
        )

        design_layout.addWidget(
            self.return_to_design_button
        )

        design_layout.addWidget(
            self.open_button
        )

        content.addWidget(design_group, 3)

    def set_project(self, project):
        """
        Display the current project's objective design picture.
        """

        self.project = project
        self.selected_objective = None
        self.selected_attention_item = None
        self._update_design_attention()

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
    def _update_design_attention(self):
        self.attention_list.clear()
        self.attention_items = []

        if self.project is None:
            self.attention_summary.setText(
                "No project is currently loaded."
            )
            return

        items = DesignAssistance(
            self.project
        ).check()

        self.attention_items = items

        if not items:
            self.attention_summary.setText(
                "No design matters currently require attention."
            )
            return

        self.attention_summary.setText(
            f"{len(items)} design matter"
            f"{'' if len(items) == 1 else 's'} "
            "may require professional attention."
        )

        for item in items:
            text = (
                f"⚠ {item.objective_title}\n"
                f"{item.title}\n"
                f"{item.message}"
            )

            self.attention_list.addItem(
                QListWidgetItem(text)
            )
    def _attention_selected(self, row):
        if (
            row < 0
            or row >= len(self.attention_items)
        ):
            return

        item = self.attention_items[row]
        self.selected_attention_item = item

        if (
            item.objective_index < 0
            or self.project is None
            or item.objective_index
            >= len(self.project.objectives)
        ):
            return

        self.objectives_list.setCurrentRow(
            item.objective_index
        )
        self._show_selected_objective()
    def _objective_clicked(self, item):
        """
        Explicitly selecting an objective returns the designer
        to the normal Design Chain view.
        """

        row = self.objectives_list.row(item)

        if (
            self.project is None
            or row < 0
            or row >= len(self.project.objectives)
        ):
            return

        self.selected_objective = (
            self.project.objectives[row]
        )

        self.selected_attention_item = None

        self._show_selected_objective()
         
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

        self.selected_attention_item = None
        self._show_selected_objective()
    def _return_to_design_chain(self):
        """
        Return from Contextual Review to the normal
        Design Chain for the selected objective.
        """

        self.selected_attention_item = None
        self._show_selected_objective()    
    def _show_selected_objective(self):
        if self.selected_objective is None:
            return

        objective = self.selected_objective
        self.return_to_design_button.setVisible(
            self.selected_attention_item is not None
        )

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

                context_text = ""

                if self.selected_attention_item is not None:
                    item = self.selected_attention_item

                    options_text = ""

                    if item.options:
                        option_lines = []

                        for option in item.options:
                            option_lines.append(
                                f"• {option.title}\n"
                                f"  {option.description}"
                            )

                        options_text = (
                            f"\n\nWHAT COULD I DO?\n"
                            f"{chr(10).join(option_lines)}"
                        )

                        context_text = (
                            f"\n\nCONTEXTUAL REVIEW\n"
                            f"⚠ {item.title}\n\n"
                            f"WHAT EXERCISE DIRECTOR NOTICED\n"
                            f"{item.message}\n\n"
                            f"WHY THIS MATTERS\n"
                            f"{item.rationale}"
                            f"{options_text}\n\n"
                            f"Exercise Director has identified a "
                            f"design condition for professional review. "
                            f"It has not selected an option or made an "
                            f"assessment of whether the objective itself "
                            f"is appropriate."
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
                            f"{context_text}"
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