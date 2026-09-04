from PySide6.QtWidgets import (
    QFrame,
    QGroupBox,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class ExerciseScopePanel(QWidget):
    """
    Workspace for defining the agreed scope of an
    exercise before detailed design begins.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.project = None

        layout = QVBoxLayout(self)

        heading = QLabel("SCOPE THE EXERCISE")
        heading.setStyleSheet(
            "font-size: 20px; "
            "font-weight: bold;"
        )

        introduction = QLabel(
            "Define what exercise is required, "
            "why it is required, and the boundaries "
            "within which it will be designed."
        )
        introduction.setWordWrap(True)

        self.project_label = QLabel(
            "No exercise project loaded."
        )
        self.project_label.setWordWrap(True)

        layout.addWidget(heading)
        layout.addWidget(introduction)
        layout.addWidget(self.project_label)

        commissioning_heading = QLabel(
            "COMMISSIONING BASIS"
        )
        commissioning_heading.setStyleSheet(
            "font-size: 14px; "
            "font-weight: bold; "
            "margin-top: 12px;"
        )
        layout.addWidget(commissioning_heading)

        commissioning_frame = QFrame()
        commissioning_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        commissioning_layout = QVBoxLayout(
            commissioning_frame
        )

        self.requirement_label = QLabel(
            "Requirement: Not recorded"
        )
        self.requirement_label.setWordWrap(True)

        self.sponsor_label = QLabel(
            "Sponsor: Not recorded"
        )
        self.sponsor_label.setWordWrap(True)

        self.operational_driver_label = QLabel(
            "Operational Driver: Not recorded"
        )
        self.operational_driver_label.setWordWrap(True)

        self.readiness_gap_label = QLabel(
            "Readiness Gap: Not recorded"
        )
        self.readiness_gap_label.setWordWrap(True)

        self.preparation_requirement_label = QLabel(
            "Preparation Requirement: Not recorded"
        )
        self.preparation_requirement_label.setWordWrap(
            True
        )

        commissioning_layout.addWidget(
            self.requirement_label
        )
        commissioning_layout.addWidget(
            self.sponsor_label
        )
        commissioning_layout.addWidget(
            self.operational_driver_label
        )
        commissioning_layout.addWidget(
            self.readiness_gap_label
        )
        commissioning_layout.addWidget(
            self.preparation_requirement_label
        )

        layout.addWidget(commissioning_frame)

        scope_group = QGroupBox(
            "EXERCISE SCOPE"
        )
        scope_layout = QVBoxLayout(
            scope_group
        )
        self.scope_tabs = QTabWidget()

        self.purpose_tab = QWidget()
        self.boundaries_tab = QWidget()
        self.approach_tab = QWidget()

        self.scope_tabs.addTab(
            self.purpose_tab,
            "1. Purpose & Aim"
        )
        self.scope_tabs.addTab(
            self.boundaries_tab,
            "2. Boundaries"
        )
        self.scope_tabs.addTab(
            self.approach_tab,
            "3. Proposed Approach"
        )

        purpose_heading = QLabel(
            "Purpose"
        )
        purpose_heading.setStyleSheet(
            "font-weight: bold;"
        )

        purpose_guidance = QLabel(
            "Why is this exercise being conducted?"
        )
        purpose_guidance.setWordWrap(True)

        self.purpose_input = QTextEdit()
        self.purpose_input.setPlaceholderText(
            "Describe the purpose of the exercise..."
        )
        self.purpose_input.setMaximumHeight(90)

        aim_heading = QLabel(
            "Aim"
        )
        aim_heading.setStyleSheet(
            "font-weight: bold;"
        )

        aim_guidance = QLabel(
            "What is the exercise intended to achieve?"
        )
        aim_guidance.setWordWrap(True)

        self.aim_input = QTextEdit()
        self.aim_input.setPlaceholderText(
            "State the overall exercise aim..."
        )
        self.aim_input.setMaximumHeight(90)
        in_scope_heading = QLabel(
            "In Scope"
        )
        in_scope_heading.setStyleSheet(
            "font-weight: bold;"
        )

        in_scope_guidance = QLabel(
            "What is included within the exercise?"
        )
        in_scope_guidance.setWordWrap(True)

        self.in_scope_input = QTextEdit()
        self.in_scope_input.setPlaceholderText(
            "Enter one item per line..."
        )
        self.in_scope_input.setMaximumHeight(100)

        out_of_scope_heading = QLabel(
            "Out of Scope"
        )
        out_of_scope_heading.setStyleSheet(
            "font-weight: bold;"
        )

        out_of_scope_guidance = QLabel(
            "What is specifically excluded from the exercise?"
        )
        out_of_scope_guidance.setWordWrap(True)

        self.out_of_scope_input = QTextEdit()
        self.out_of_scope_input.setPlaceholderText(
            "Enter one item per line..."
        )
        self.out_of_scope_input.setMaximumHeight(100)
        constraints_heading = QLabel(
            "Constraints"
        )
        constraints_heading.setStyleSheet(
            "font-weight: bold;"
        )

        constraints_guidance = QLabel(
            "What constraints must the exercise "
            "be designed within?"
        )
        constraints_guidance.setWordWrap(True)

        self.constraints_input = QTextEdit()
        self.constraints_input.setPlaceholderText(
            "Enter one item per line..."
        )
        self.constraints_input.setMaximumHeight(100)

        assumptions_heading = QLabel(
            "Assumptions"
        )
        assumptions_heading.setStyleSheet(
            "font-weight: bold;"
        )

        assumptions_guidance = QLabel(
            "What assumptions underpin the "
            "exercise scope?"
        )
        assumptions_guidance.setWordWrap(True)

        self.assumptions_input = QTextEdit()
        self.assumptions_input.setPlaceholderText(
            "Enter one item per line..."
        )
        self.assumptions_input.setMaximumHeight(100)        

        self.save_scope_button = QPushButton(
            "Save Scope"
        )
        self.save_scope_button.clicked.connect(
        self._save_scope
        )
        self.save_confirmation_label = QLabel("")
        self.save_confirmation_label.setStyleSheet(
            "font-weight: bold;"
        )


        purpose_layout = QVBoxLayout(
            self.purpose_tab
        )

        purpose_layout.addWidget(purpose_heading)
        purpose_layout.addWidget(purpose_guidance)
        purpose_layout.addWidget(self.purpose_input)
        purpose_layout.addWidget(aim_heading)
        purpose_layout.addWidget(aim_guidance)
        purpose_layout.addWidget(self.aim_input)

        boundaries_layout = QVBoxLayout(
            self.boundaries_tab
        )

        boundaries_layout.addWidget(in_scope_heading)
        boundaries_layout.addWidget(in_scope_guidance)
        boundaries_layout.addWidget(
            self.in_scope_input
        )

        boundaries_layout.addWidget(
            out_of_scope_heading
        )
        boundaries_layout.addWidget(
            constraints_heading
        )
        boundaries_layout.addWidget(
            constraints_guidance
        )
        boundaries_layout.addWidget(
            self.constraints_input
        )

        boundaries_layout.addWidget(
            assumptions_heading
        )
        boundaries_layout.addWidget(
            assumptions_guidance
        )
        boundaries_layout.addWidget(
            self.assumptions_input
        )
        boundaries_layout.addWidget(
            out_of_scope_guidance
        )
        boundaries_layout.addWidget(
            self.out_of_scope_input
        )

        scope_layout.addWidget(
            self.save_scope_button
        )
        scope_layout.addWidget(
        self.scope_tabs
        )
        approach_layout = QVBoxLayout(
                self.approach_tab
            )

        exercise_type_heading = QLabel(
            "Exercise Type"
        )
        exercise_type_heading.setStyleSheet(
            "font-weight: bold;"
        )

        exercise_type_guidance = QLabel(
            "What type or format of exercise is proposed?"
        )
        exercise_type_guidance.setWordWrap(True)

        self.exercise_type_input = QTextEdit()
        self.exercise_type_input.setPlaceholderText(
            "Describe the proposed exercise type "
            "or format..."
        )
        self.exercise_type_input.setMaximumHeight(80)

        approach_layout.addWidget(
            exercise_type_heading
        )
        approach_layout.addWidget(
            exercise_type_guidance
        )
        approach_layout.addWidget(
            self.exercise_type_input
        )
        proposed_approach_heading = QLabel(
            "Proposed Approach"
        )
        proposed_approach_heading.setStyleSheet(
            "font-weight: bold;"
        )

        proposed_approach_guidance = QLabel(
            "How is the exercise proposed to be "
            "structured and delivered?"
        )
        proposed_approach_guidance.setWordWrap(True)

        self.proposed_approach_input = QTextEdit()
        self.proposed_approach_input.setPlaceholderText(
            "Describe the broad exercise approach..."
        )
        self.proposed_approach_input.setMaximumHeight(110)

        approach_layout.addWidget(
            proposed_approach_heading
        )
        approach_layout.addWidget(
            proposed_approach_guidance
        )
        approach_layout.addWidget(
            self.proposed_approach_input
        )
        scenario_heading = QLabel(
            "Scenario Proposition"
        )
        scenario_heading.setStyleSheet(
            "font-weight: bold;"
        )

        scenario_guidance = QLabel(
            "What broad scenario will create the "
            "conditions required by the exercise?"
        )
        scenario_guidance.setWordWrap(True)

        self.scenario_proposition_input = QTextEdit()
        self.scenario_proposition_input.setPlaceholderText(
            "Describe the broad scenario proposition..."
        )
        self.scenario_proposition_input.setMaximumHeight(110)

        approach_layout.addWidget(
            scenario_heading
        )
        approach_layout.addWidget(
            scenario_guidance
        )
        approach_layout.addWidget(
            self.scenario_proposition_input
        )
        end_state_heading = QLabel(
            "Intended End State"
        )
        end_state_heading.setStyleSheet(
            "font-weight: bold;"
        )

        end_state_guidance = QLabel(
            "Where should the exercise conclude, "
            "and what should have been demonstrated?"
        )
        end_state_guidance.setWordWrap(True)

        self.intended_end_state_input = QTextEdit()
        self.intended_end_state_input.setPlaceholderText(
            "Describe the intended exercise end state..."
        )
        self.intended_end_state_input.setMaximumHeight(110)

        approach_layout.addWidget(
            end_state_heading
        )
        approach_layout.addWidget(
            end_state_guidance
        )
        approach_layout.addWidget(
            self.intended_end_state_input
        )
        approach_layout.addStretch()
            
        scope_layout.addWidget(
            self.save_confirmation_label
        )
        layout.addWidget(scope_group)
        layout.addStretch()
    def set_project(self, project):
        self.project = project

        if project is None:
            self.project_label.setText(
                "No exercise project loaded."
            )
            self.requirement_label.setText(
                "Requirement: Not recorded"
            )
            self.sponsor_label.setText(
                "Sponsor: Not recorded"
            )
            self.operational_driver_label.setText(
                "Operational Driver: Not recorded"
            )
            self.readiness_gap_label.setText(
                "Readiness Gap: Not recorded"
            )
            self.preparation_requirement_label.setText(
                "Preparation Requirement: Not recorded"
            )
            return

        project_name = (
            getattr(project, "name", "")
            or "Untitled Project"
        )

        self.project_label.setText(
            f"Current Exercise: {project_name}"
        )
        scope = project.exercise_scope

        self.purpose_input.setPlainText(
            scope.purpose
        )

        self.aim_input.setPlainText(
            scope.aim
        )
        self.in_scope_input.setPlainText(
            "\n".join(scope.in_scope)
        )

        self.out_of_scope_input.setPlainText(
        "\n".join(scope.out_of_scope)
        )
        self.constraints_input.setPlainText(
            "\n".join(scope.constraints)
        )

        self.assumptions_input.setPlainText(
            "\n".join(scope.assumptions)
        )
        self.exercise_type_input.setPlainText(
            scope.exercise_type
        )
        self.proposed_approach_input.setPlainText(
            scope.proposed_approach
        )
        self.scenario_proposition_input.setPlainText(
            scope.scenario_proposition
        )
        self.intended_end_state_input.setPlainText(
            scope.intended_end_state
        )
        requirement = project.operational_requirement
        readiness = requirement.readiness
        readiness_gap = readiness.readiness_gap
        if isinstance(readiness_gap, str):
            readiness_gap_shortfall = readiness_gap
            preparation_requirement = ""
        else:
            readiness_gap_shortfall = (
                readiness_gap.shortfall
            )
            preparation_requirement = (
                readiness_gap.preparation_requirement
    )

        self.requirement_label.setText(
            "Requirement: "
            f"{requirement.description or 'Not recorded'}"
        )

        self.sponsor_label.setText(
            "Sponsor: "
            f"{requirement.sponsor or 'Not recorded'}"
        )

        self.operational_driver_label.setText(
            "Operational Driver: "
            f"{requirement.operational_driver or 'Not recorded'}"
        )

        self.readiness_gap_label.setText(
            "Readiness Gap: "
            f"{readiness_gap_shortfall or 'Not recorded'}"
        )

        self.preparation_requirement_label.setText(
            "Preparation Requirement: "
            f"{preparation_requirement or 'Not recorded'}"
        )
    def _save_scope(self):
        if self.project is None:
            self.purpose_input.clear()
            self.aim_input.clear()
            self.in_scope_input.clear()
            self.out_of_scope_input.clear()
            self.constraints_input.clear()
            self.assumptions_input.clear()
            self.exercise_type_input.clear()
            self.proposed_approach_input.clear()
            self.scenario_proposition_input.clear()
            self.intended_end_state_input.clear()
            return

        scope = self.project.exercise_scope

        scope.purpose = (
            self.purpose_input
            .toPlainText()
            .strip()
        )

        scope.aim = (
            self.aim_input
            .toPlainText()
            .strip()
        )
        scope.in_scope = [
            item.strip()
            for item in (
                self.in_scope_input
                .toPlainText()
                .splitlines()
            )
            if item.strip()
        ]

        scope.out_of_scope = [
            item.strip()
            for item in (
                self.out_of_scope_input
                .toPlainText()
                .splitlines()
            )
            if item.strip()
        ]
        scope.constraints = [
            item.strip()
            for item in (
                self.constraints_input
                .toPlainText()
                .splitlines()
            )
            if item.strip()
        ]

        scope.assumptions = [
            item.strip()
            for item in (
                self.assumptions_input
                .toPlainText()
                .splitlines()
            )
            if item.strip()
        ]
        self.save_confirmation_label.setText(
            "Scope changes recorded"
        )
        scope.exercise_type = (
            self.exercise_type_input
            .toPlainText()
            .strip()
        )
        scope.proposed_approach = (
            self.proposed_approach_input
            .toPlainText()
            .strip()
        )
        scope.scenario_proposition = (
            self.scenario_proposition_input
            .toPlainText()
            .strip()
        )
        scope.intended_end_state = (
            self.intended_end_state_input
            .toPlainText()
            .strip()
        )