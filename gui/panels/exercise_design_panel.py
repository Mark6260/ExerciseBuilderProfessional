from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QScrollArea,
    QSizePolicy,
    QMessageBox,
    QLabel,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.exercise_design_opportunity import ExerciseDesignOpportunity
from core.candidate_exercise_activity import CandidateExerciseActivity


class ExerciseDesignPanel(QWidget):
    """
    Derived exercise-design view built from the assured CTO.

    This panel does not create or alter the CTO. It translates the
    Project-owned CTO into exercise design requirements so the designer
    can see what the exercise must create opportunities to demonstrate
    and what evidence the exercise must be capable of producing.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.project = None
        self.cto = None

        self._build_ui()

    def _build_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        page = QWidget()
        page.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.MinimumExpanding,
        )

        layout = QVBoxLayout(page)
        layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )
        layout.setSpacing(12)

        title = QLabel(
            "EXERCISE DESIGN FROM ASSURED CTO"
        )
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )
        layout.addWidget(title)

        guidance = QLabel(
            "Translate the assured Collective Training Objective into "
            "requirements for exercise design. Exercise Director shows "
            "what the exercise must create an opportunity to demonstrate "
            "and what evidence it must be capable of producing."
        )
        guidance.setWordWrap(True)
        layout.addWidget(guidance)

        status_frame = QFrame()
        status_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )
        status_layout = QVBoxLayout(
            status_frame
        )

        self.status_label = QLabel(
            "No project loaded"
        )
        self.status_label.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        self.status_label.setWordWrap(True)

        self.status_detail = QLabel("")
        self.status_detail.setWordWrap(True)

        status_layout.addWidget(
            self.status_label
        )
        status_layout.addWidget(
            self.status_detail
        )

        layout.addWidget(
            status_frame
        )

        self.design_tree = QTreeWidget()
        self.design_tree.setColumnCount(3)
        self.design_tree.setHeaderLabels(
            [
                "Design Level",
                "Assured Requirement",
                "Exercise Design Implication",
            ]
        )
        self.design_tree.setAlternatingRowColors(
            True
        )
        self.design_tree.setRootIsDecorated(
            True
        )
        self.design_tree.setUniformRowHeights(
            False
        )

        self.design_tree.header().setStretchLastSection(
            True
        )

        self.design_tree.setColumnWidth(
            0,
            190,
        )
        self.design_tree.setColumnWidth(
            1,
            430,
        )

        layout.addWidget(
            self.design_tree,
            1,
        )

        opportunity_frame = QFrame()
        opportunity_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )
        opportunity_layout = QVBoxLayout(
            opportunity_frame
        )

        opportunity_title = QLabel(
            "DESIGN OPPORTUNITY"
        )
        opportunity_title.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        opportunity_layout.addWidget(
            opportunity_title
        )

        opportunity_guidance = QLabel(
            "Select a Success Factor in the assured design tree, then "
            "describe a credible situation or activity that gives the "
            "training audience a fair opportunity to demonstrate it. "
            "Do not write an inject here."
        )
        opportunity_guidance.setWordWrap(True)
        opportunity_layout.addWidget(
            opportunity_guidance
        )

        self.selected_requirement_label = QLabel(
            "Selected Success Factor: None"
        )
        self.selected_requirement_label.setWordWrap(
            True
        )
        opportunity_layout.addWidget(
            self.selected_requirement_label
        )

        self.opportunity_title_input = QLineEdit()
        self.opportunity_title_input.setPlaceholderText(
            "e.g. Competing operational demands require HQ coordination"
        )
        opportunity_layout.addWidget(
            self.opportunity_title_input
        )

        self.opportunity_description_input = QTextEdit()
        self.opportunity_description_input.setPlaceholderText(
            "Describe the exercise situation or activity. What must be "
            "happening so the collective has a credible opportunity to "
            "demonstrate the selected success factor?"
        )
        self.opportunity_description_input.setFixedHeight(
            90
        )
        opportunity_layout.addWidget(
            self.opportunity_description_input
        )

        self.add_opportunity_button = QPushButton(
            "ADD DESIGN OPPORTUNITY"
        )
        self.add_opportunity_button.setEnabled(
            False
        )
        self.add_opportunity_button.clicked.connect(
            self._add_design_opportunity
        )
        opportunity_layout.addWidget(
            self.add_opportunity_button
        )

        self.opportunity_tree = QTreeWidget()
        self.opportunity_tree.setColumnCount(
            3
        )
        self.opportunity_tree.setHeaderLabels(
            [
                "Design Opportunity",
                "Assured Link",
                "Coverage",
            ]
        )
        self.opportunity_tree.setMinimumHeight(
            150
        )
        self.opportunity_tree.header().setStretchLastSection(
            True
        )
        self.opportunity_tree.setColumnWidth(
            0,
            300,
        )
        self.opportunity_tree.setColumnWidth(
            1,
            520,
        )
        opportunity_layout.addWidget(
            self.opportunity_tree
        )

        self.opportunity_tree.itemSelectionChanged.connect(
            self._opportunity_selected
        )

        layout.addWidget(
            opportunity_frame
        )

        self.design_tree.itemSelectionChanged.connect(
            self._design_requirement_selected
        )
        self.opportunity_title_input.textChanged.connect(
            self._update_add_opportunity_button
        )
        self.opportunity_description_input.textChanged.connect(
            self._update_add_opportunity_button
        )

        decomposition_frame = QFrame()
        decomposition_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )
        decomposition_layout = QVBoxLayout(
            decomposition_frame
        )

        decomposition_title = QLabel(
            "DESIGN OPPORTUNITY DECOMPOSITION"
        )
        decomposition_title.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        decomposition_layout.addWidget(
            decomposition_title
        )

        decomposition_guidance = QLabel(
            "Select a Design Opportunity above, then define the design "
            "ingredients that later MEL/MIL activity must provide. "
            "Stay at requirement level here — do not write individual "
            "injects yet."
        )
        decomposition_guidance.setWordWrap(True)
        decomposition_layout.addWidget(
            decomposition_guidance
        )

        self.selected_opportunity_label = QLabel(
            "Selected Design Opportunity: None"
        )
        self.selected_opportunity_label.setWordWrap(
            True
        )
        decomposition_layout.addWidget(
            self.selected_opportunity_label
        )

        conditions_label = QLabel(
            "REQUIRED CONDITIONS"
        )
        conditions_label.setStyleSheet(
            "font-weight: bold;"
        )
        decomposition_layout.addWidget(
            conditions_label
        )

        self.required_conditions_input = QTextEdit()
        self.required_conditions_input.setPlaceholderText(
            "What conditions, pressures, constraints or context must "
            "exist for this opportunity to be credible?"
        )
        self.required_conditions_input.setFixedHeight(
            70
        )
        decomposition_layout.addWidget(
            self.required_conditions_input
        )

        stimulus_label = QLabel(
            "STIMULUS / INFORMATION"
        )
        stimulus_label.setStyleSheet(
            "font-weight: bold;"
        )
        decomposition_layout.addWidget(
            stimulus_label
        )

        self.stimulus_information_input = QTextEdit()
        self.stimulus_information_input.setPlaceholderText(
            "What information, event, report, request or change must "
            "reach the training audience? Describe the requirement, "
            "not the wording of an inject."
        )
        self.stimulus_information_input.setFixedHeight(
            70
        )
        decomposition_layout.addWidget(
            self.stimulus_information_input
        )

        response_label = QLabel(
            "RESPONSE OPPORTUNITY"
        )
        response_label.setStyleSheet(
            "font-weight: bold;"
        )
        decomposition_layout.addWidget(
            response_label
        )

        self.response_opportunity_input = QTextEdit()
        self.response_opportunity_input.setPlaceholderText(
            "What must the exercise allow the training audience to do, "
            "decide, coordinate or produce so performance can be observed?"
        )
        self.response_opportunity_input.setFixedHeight(
            70
        )
        decomposition_layout.addWidget(
            self.response_opportunity_input
        )

        evidence_label = QLabel(
            "EVIDENCE / CAPTURE REQUIREMENT"
        )
        evidence_label.setStyleSheet(
            "font-weight: bold;"
        )
        decomposition_layout.addWidget(
            evidence_label
        )

        self.evidence_capture_input = QTextEdit()
        self.evidence_capture_input.setPlaceholderText(
            "How must ExCon or observers be able to capture the assured "
            "evidence during this opportunity?"
        )
        self.evidence_capture_input.setFixedHeight(
            70
        )
        decomposition_layout.addWidget(
            self.evidence_capture_input
        )

        self.save_decomposition_button = QPushButton(
            "SAVE DESIGN DECOMPOSITION"
        )
        self.save_decomposition_button.setEnabled(
            False
        )
        self.save_decomposition_button.clicked.connect(
            self._save_design_decomposition
        )
        decomposition_layout.addWidget(
            self.save_decomposition_button
        )

        layout.addWidget(
            decomposition_frame
        )

        activity_frame = QFrame()
        activity_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )
        activity_layout = QVBoxLayout(
            activity_frame
        )

        activity_title = QLabel(
            "CANDIDATE EXERCISE ACTIVITY"
        )
        activity_title.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        activity_layout.addWidget(
            activity_title
        )

        activity_guidance = QLabel(
            "Select a completed Design Opportunity above, then describe "
            "a candidate piece of exercise architecture that could create "
            "that opportunity. This is still not an inject or MEL/MIL row."
        )
        activity_guidance.setWordWrap(
            True
        )
        activity_layout.addWidget(
            activity_guidance
        )

        self.selected_activity_opportunity_label = QLabel(
            "Selected Design Opportunity: None"
        )
        self.selected_activity_opportunity_label.setWordWrap(
            True
        )
        activity_layout.addWidget(
            self.selected_activity_opportunity_label
        )

        self.candidate_activity_title_input = QLineEdit()
        self.candidate_activity_title_input.setPlaceholderText(
            "e.g. Concurrent incident coordination sequence"
        )
        activity_layout.addWidget(
            self.candidate_activity_title_input
        )

        self.candidate_activity_method_input = QComboBox()
        self.candidate_activity_method_input.addItems(
            [
                "Select delivery method...",
                "Facilitated discussion",
                "Scripted role-play",
                "Simulated operational activity",
                "Live activity",
                "Decision point",
                "Information flow / reporting",
                "Control-cell interaction",
                "Other",
            ]
        )
        activity_layout.addWidget(
            self.candidate_activity_method_input
        )

        self.candidate_activity_phase_input = QLineEdit()
        self.candidate_activity_phase_input.setPlaceholderText(
            "Phase / placement (optional)"
        )
        activity_layout.addWidget(
            self.candidate_activity_phase_input
        )

        self.candidate_activity_description_input = QTextEdit()
        self.candidate_activity_description_input.setPlaceholderText(
            "Describe the candidate activity at exercise-architecture "
            "level. What would happen, who would be involved, and how "
            "would it create the required design opportunity?"
        )
        self.candidate_activity_description_input.setFixedHeight(
            85
        )
        activity_layout.addWidget(
            self.candidate_activity_description_input
        )

        self.candidate_activity_notes_input = QTextEdit()
        self.candidate_activity_notes_input.setPlaceholderText(
            "Designer notes (optional) — constraints, dependencies, "
            "resources or realism considerations."
        )
        self.candidate_activity_notes_input.setFixedHeight(
            60
        )
        activity_layout.addWidget(
            self.candidate_activity_notes_input
        )

        self.add_candidate_activity_button = QPushButton(
            "ADD CANDIDATE EXERCISE ACTIVITY"
        )
        self.add_candidate_activity_button.setEnabled(
            False
        )
        self.add_candidate_activity_button.clicked.connect(
            self._add_candidate_exercise_activity
        )
        activity_layout.addWidget(
            self.add_candidate_activity_button
        )

        self.candidate_activity_tree = QTreeWidget()
        self.candidate_activity_tree.setColumnCount(
            4
        )
        self.candidate_activity_tree.setHeaderLabels(
            [
                "Candidate Activity",
                "Design Opportunity",
                "Delivery Method",
                "Assurance Coverage",
            ]
        )
        self.candidate_activity_tree.setMinimumHeight(
            150
        )
        self.candidate_activity_tree.header().setStretchLastSection(
            True
        )
        self.candidate_activity_tree.setColumnWidth(
            0,
            300,
        )
        self.candidate_activity_tree.setColumnWidth(
            1,
            360,
        )
        self.candidate_activity_tree.setColumnWidth(
            2,
            220,
        )

        activity_layout.addWidget(
            self.candidate_activity_tree
        )

        layout.addWidget(
            activity_frame
        )

        self.candidate_activity_title_input.textChanged.connect(
            self._update_add_candidate_activity_button
        )
        self.candidate_activity_description_input.textChanged.connect(
            self._update_add_candidate_activity_button
        )
        self.candidate_activity_method_input.currentIndexChanged.connect(
            self._update_add_candidate_activity_button
        )

        footer_layout = QHBoxLayout()

        self.refresh_button = QPushButton(
            "REFRESH FROM CTO"
        )
        self.refresh_button.clicked.connect(
            self.refresh_view
        )

        footer_layout.addStretch()
        footer_layout.addWidget(
            self.refresh_button
        )

        layout.addLayout(
            footer_layout
        )

        # Preserve useful editor heights. As Exercise Design grows,
        # the workspace scrolls instead of crushing stacked controls.
        layout.setSizeConstraint(
            QVBoxLayout.SizeConstraint.SetMinimumSize
        )

        scroll_area.setWidget(page)
        outer_layout.addWidget(scroll_area)

    def set_project(
        self,
        project,
    ):
        self.project = project
        self.refresh_view()

    def refresh_view(self):
        self.design_tree.clear()
        self.opportunity_tree.clear()
        self.candidate_activity_tree.clear()
        self._clear_candidate_activity_editor()
        self._clear_decomposition_editor()
        self.selected_requirement_label.setText(
            "Selected Success Factor: None"
        )
        self.add_opportunity_button.setEnabled(
            False
        )
        self.cto = None

        if self.project is None:
            self.status_label.setText(
                "NO PROJECT LOADED"
            )
            self.status_detail.setText(
                "Open or create an Exercise Director project."
            )
            return

        if not self.project.collective_training_objectives:
            self.status_label.setText(
                "NO CTO AVAILABLE"
            )
            self.status_detail.setText(
                "Complete the CTO Builder before exercise design begins."
            )
            return

        self.cto = (
            self.project.collective_training_objectives[0]
        )

        structure_ready = (
            self.cto.passes_collective_structure_test()
        )
        success_ready = (
            self.cto.has_evidence_coverage()
        )
        critical_ready = (
            self.cto.has_critical_error_coverage()
        )

        ready = (
            structure_ready
            and success_ready
            and critical_ready
        )

        if not ready:
            self.status_label.setText(
                "CTO NEEDS DEVELOPMENT"
            )
            self.status_detail.setText(
                "Exercise design is not yet released from the CTO "
                "assurance gate. Resolve the gaps identified in the "
                "CTO Design Review first."
            )
            self._show_blocking_gaps()
            return

        self.status_label.setText(
            "READY FOR EXERCISE DESIGN"
        )
        self.status_detail.setText(
            "The CTO has passed the current structural and evidence "
            "coverage checks. The requirements below are derived from "
            "that assured design basis. Professional judgement remains "
            "with the Exercise Director."
        )

        self._build_design_requirements()
        self.design_tree.expandAll()
        self._refresh_design_opportunities()
        self._refresh_candidate_activities()

    def _show_blocking_gaps(self):
        root = QTreeWidgetItem(
            [
                "Assurance Gate",
                "CTO is not ready for exercise design",
                "Return to CTO Builder → Design Review",
            ]
        )
        self.design_tree.addTopLevelItem(
            root
        )

        for reason in self.cto.collective_test_reasons():
            QTreeWidgetItem(
                root,
                [
                    "Structure Gap",
                    reason,
                    "Resolve before exercise design.",
                ],
            )

        for task in self.cto.collective_tasks:
            for factor in task.success_factors:
                if not factor.metrics:
                    item = QTreeWidgetItem(
                        root,
                        [
                            "Evidence Gap",
                            factor.description,
                            (
                                "Define at least one observable metric "
                                f"for task: {task.title}."
                            ),
                        ],
                    )
                    item.setData(
                        0,
                        Qt.ItemDataRole.UserRole,
                        factor.id,
                    )
                    continue

                for metric in factor.metrics:
                    if not metric.evidence_requirements:
                        item = QTreeWidgetItem(
                            root,
                            [
                                "Evidence Gap",
                                metric.description,
                                (
                                    "Define the evidence the exercise "
                                    "must be capable of producing."
                                ),
                            ],
                        )
                        item.setData(
                            0,
                            Qt.ItemDataRole.UserRole,
                            metric.id,
                        )

        for task in self.cto.collective_tasks:
            for error in task.critical_errors:
                if not error.metrics:
                    item = QTreeWidgetItem(
                        root,
                        [
                            "Critical Error Gap",
                            error.description,
                            (
                                "Define how this critical failure would "
                                "be observed."
                            ),
                        ],
                    )
                    item.setData(
                        0,
                        Qt.ItemDataRole.UserRole,
                        error.id,
                    )
                    continue

                for metric in error.metrics:
                    if not metric.evidence_requirements:
                        item = QTreeWidgetItem(
                            root,
                            [
                                "Critical Error Gap",
                                metric.description,
                                (
                                    "Define evidence for this critical "
                                    "error metric."
                                ),
                            ],
                        )
                        item.setData(
                            0,
                            Qt.ItemDataRole.UserRole,
                            metric.id,
                        )

        self.design_tree.expandAll()

    def _build_design_requirements(self):
        cto_item = QTreeWidgetItem(
            [
                "Collective Outcome",
                self.cto.required_outcome,
                (
                    "The exercise must create a credible opportunity "
                    "for the training audience to demonstrate this "
                    "collective outcome."
                ),
            ]
        )
        cto_item.setData(
            0,
            Qt.ItemDataRole.UserRole,
            self.cto.id,
        )

        self.design_tree.addTopLevelItem(
            cto_item
        )

        for task in self.cto.collective_tasks:
            task_item = QTreeWidgetItem(
                cto_item,
                [
                    "Collective Task",
                    task.title,
                    (
                        "Create one or more exercise activities or "
                        "situations that require the collective to "
                        "perform this task."
                    ),
                ],
            )
            task_item.setData(
                0,
                Qt.ItemDataRole.UserRole,
                task.id,
            )

            for factor in task.success_factors:
                factor_item = QTreeWidgetItem(
                    task_item,
                    [
                        "Success Factor",
                        factor.description,
                        (
                            "Design the situation so successful "
                            "collective performance can be demonstrated."
                        ),
                    ],
                )
                factor_item.setData(
                    0,
                    Qt.ItemDataRole.UserRole,
                    factor.id,
                )
                factor_item.setData(
                    1,
                    Qt.ItemDataRole.UserRole,
                    "success_factor",
                )
                factor_item.setData(
                    2,
                    Qt.ItemDataRole.UserRole,
                    {
                        "task_id": task.id,
                        "task_title": task.title,
                        "factor_id": factor.id,
                        "factor_description": factor.description,
                    },
                )

                for metric in factor.metrics:
                    metric_item = QTreeWidgetItem(
                        factor_item,
                        [
                            "Observable Metric",
                            metric.description,
                            (
                                "Ensure observers can see, hear, record "
                                "or measure this during exercise play."
                            ),
                        ],
                    )
                    metric_item.setData(
                        0,
                        Qt.ItemDataRole.UserRole,
                        metric.id,
                    )

                    for requirement in metric.evidence_requirements:
                        evidence_item = QTreeWidgetItem(
                            metric_item,
                            [
                                "Evidence Requirement",
                                requirement.description,
                                (
                                    "Exercise design must enable this "
                                    "evidence to be produced or captured"
                                    + (
                                        f" ({requirement.evidence_type})."
                                        if requirement.evidence_type
                                        else "."
                                    )
                                ),
                            ],
                        )
                        evidence_item.setData(
                            0,
                            Qt.ItemDataRole.UserRole,
                            requirement.id,
                        )

            for error in task.critical_errors:
                error_item = QTreeWidgetItem(
                    task_item,
                    [
                        "Critical Error",
                        error.description,
                        (
                            "Where appropriate, design conditions that "
                            "allow this serious failure to be recognised "
                            "without artificially forcing it to occur."
                        ),
                    ],
                )
                error_item.setData(
                    0,
                    Qt.ItemDataRole.UserRole,
                    error.id,
                )

                for metric in error.metrics:
                    metric_item = QTreeWidgetItem(
                        error_item,
                        [
                            "Critical Error Metric",
                            metric.description,
                            (
                                "Ensure observers can recognise this "
                                "failure if it occurs."
                            ),
                        ],
                    )
                    metric_item.setData(
                        0,
                        Qt.ItemDataRole.UserRole,
                        metric.id,
                    )

                    for requirement in metric.evidence_requirements:
                        evidence_item = QTreeWidgetItem(
                            metric_item,
                            [
                                "Evidence Requirement",
                                requirement.description,
                                (
                                    "Ensure this evidence can be captured "
                                    "if the critical error occurs"
                                    + (
                                        f" ({requirement.evidence_type})."
                                        if requirement.evidence_type
                                        else "."
                                    )
                                ),
                            ],
                        )
                        evidence_item.setData(
                            0,
                            Qt.ItemDataRole.UserRole,
                            requirement.id,
                        )

    def _design_requirement_selected(self):
        items = self.design_tree.selectedItems()

        if not items:
            self.selected_requirement_label.setText(
                "Selected Success Factor: None"
            )
            self._update_add_opportunity_button()
            return

        item = items[0]
        item_type = item.data(
            1,
            Qt.ItemDataRole.UserRole,
        )

        if item_type != "success_factor":
            self.selected_requirement_label.setText(
                "Selected Success Factor: None — select a Success Factor "
                "row in the assured design tree."
            )
            self._update_add_opportunity_button()
            return

        data = item.data(
            2,
            Qt.ItemDataRole.UserRole,
        ) or {}

        self.selected_requirement_label.setText(
            "Selected Success Factor: "
            + data.get(
                "factor_description",
                "",
            )
        )

        self._update_add_opportunity_button()

    def _selected_success_factor_data(self):
        items = self.design_tree.selectedItems()

        if not items:
            return None

        item = items[0]

        if item.data(
            1,
            Qt.ItemDataRole.UserRole,
        ) != "success_factor":
            return None

        return item.data(
            2,
            Qt.ItemDataRole.UserRole,
        )

    def _update_add_opportunity_button(self):
        selected = self._selected_success_factor_data()

        enabled = bool(
            self.project is not None
            and self.cto is not None
            and selected
            and self.opportunity_title_input.text().strip()
            and self.opportunity_description_input.toPlainText().strip()
            and self.cto.passes_collective_structure_test()
            and self.cto.has_evidence_coverage()
            and self.cto.has_critical_error_coverage()
        )

        self.add_opportunity_button.setEnabled(
            enabled
        )

    def _find_success_factor(
        self,
        task_id,
        factor_id,
    ):
        for task in self.cto.collective_tasks:
            if task.id != task_id:
                continue

            for factor in task.success_factors:
                if factor.id == factor_id:
                    return task, factor

        return None, None

    def _add_design_opportunity(self):
        selected = self._selected_success_factor_data()

        if not selected:
            return

        task, factor = self._find_success_factor(
            selected.get(
                "task_id",
                "",
            ),
            selected.get(
                "factor_id",
                "",
            ),
        )

        if task is None or factor is None:
            QMessageBox.warning(
                self,
                "Design Opportunity",
                "The selected assured requirement could not be found.",
            )
            return

        metric_ids = [
            metric.id
            for metric in factor.metrics
        ]

        evidence_ids = [
            requirement.id
            for metric in factor.metrics
            for requirement in metric.evidence_requirements
        ]

        opportunity = ExerciseDesignOpportunity(
            title=self.opportunity_title_input.text().strip(),
            description=(
                self.opportunity_description_input
                .toPlainText()
                .strip()
            ),
            cto_id=self.cto.id,
            collective_task_id=task.id,
            success_factor_id=factor.id,
            metric_ids=metric_ids,
            evidence_requirement_ids=evidence_ids,
        )

        self.project.add_exercise_design_opportunity(
            opportunity
        )

        self.opportunity_title_input.clear()
        self.opportunity_description_input.clear()

        self._refresh_design_opportunities()
        self._update_add_opportunity_button()

    def _refresh_design_opportunities(self):
        self.opportunity_tree.clear()

        if self.project is None or self.cto is None:
            return

        opportunities = [
            opportunity
            for opportunity in self.project.exercise_design_opportunities
            if opportunity.cto_id == self.cto.id
        ]

        for opportunity in opportunities:
            task, factor = self._find_success_factor(
                opportunity.collective_task_id,
                opportunity.success_factor_id,
            )

            if factor is None:
                assured_link = "Assured requirement no longer found"
                coverage = "Review required"
            else:
                assured_link = (
                    f"{task.title} → {factor.description}"
                )

                metric_count = len(
                    opportunity.metric_ids
                )
                evidence_count = len(
                    opportunity.evidence_requirement_ids
                )

                decomposition_complete = all(
                    [
                        opportunity.required_conditions.strip(),
                        opportunity.stimulus_information.strip(),
                        opportunity.response_opportunity.strip(),
                        opportunity.evidence_capture_plan.strip(),
                    ]
                )

                coverage = (
                    f"{metric_count} metric(s), "
                    f"{evidence_count} evidence requirement(s) | "
                    + (
                        "Decomposition complete"
                        if decomposition_complete
                        else "Decomposition needed"
                    )
                )

            item = QTreeWidgetItem(
                [
                    opportunity.title,
                    assured_link,
                    coverage,
                ]
            )
            item.setToolTip(
                0,
                opportunity.description,
            )
            item.setData(
                0,
                Qt.ItemDataRole.UserRole,
                opportunity.id,
            )

            self.opportunity_tree.addTopLevelItem(
                item
            )

    def _clear_decomposition_editor(self):
        if not hasattr(
            self,
            "selected_opportunity_label",
        ):
            return

        self.selected_opportunity_label.setText(
            "Selected Design Opportunity: None"
        )
        self.required_conditions_input.clear()
        self.stimulus_information_input.clear()
        self.response_opportunity_input.clear()
        self.evidence_capture_input.clear()
        self.save_decomposition_button.setEnabled(
            False
        )

    def _selected_design_opportunity(self):
        if self.project is None:
            return None

        items = self.opportunity_tree.selectedItems()

        if not items:
            return None

        opportunity_id = items[0].data(
            0,
            Qt.ItemDataRole.UserRole,
        )

        for opportunity in self.project.exercise_design_opportunities:
            if opportunity.id == opportunity_id:
                return opportunity

        return None

    def _opportunity_selected(self):
        opportunity = self._selected_design_opportunity()

        if opportunity is None:
            self._clear_decomposition_editor()
            self._clear_candidate_activity_editor()
            return

        self.selected_opportunity_label.setText(
            "Selected Design Opportunity: "
            + opportunity.title
        )

        self.selected_activity_opportunity_label.setText(
            "Selected Design Opportunity: "
            + opportunity.title
        )

        self.required_conditions_input.setPlainText(
            opportunity.required_conditions
        )
        self.stimulus_information_input.setPlainText(
            opportunity.stimulus_information
        )
        self.response_opportunity_input.setPlainText(
            opportunity.response_opportunity
        )
        self.evidence_capture_input.setPlainText(
            opportunity.evidence_capture_plan
        )

        self.save_decomposition_button.setEnabled(
            True
        )
        self._update_add_candidate_activity_button()

    def _save_design_decomposition(self):
        opportunity = self._selected_design_opportunity()

        if opportunity is None:
            return

        opportunity.required_conditions = (
            self.required_conditions_input
            .toPlainText()
            .strip()
        )
        opportunity.stimulus_information = (
            self.stimulus_information_input
            .toPlainText()
            .strip()
        )
        opportunity.response_opportunity = (
            self.response_opportunity_input
            .toPlainText()
            .strip()
        )
        opportunity.evidence_capture_plan = (
            self.evidence_capture_input
            .toPlainText()
            .strip()
        )

        selected_id = opportunity.id

        self._refresh_design_opportunities()

        for index in range(
            self.opportunity_tree.topLevelItemCount()
        ):
            item = self.opportunity_tree.topLevelItem(
                index
            )
            if item.data(
                0,
                Qt.ItemDataRole.UserRole,
            ) == selected_id:
                self.opportunity_tree.setCurrentItem(
                    item
                )
                break

        self._update_add_candidate_activity_button()

    def _clear_candidate_activity_editor(self):
        if not hasattr(
            self,
            "selected_activity_opportunity_label",
        ):
            return

        self.selected_activity_opportunity_label.setText(
            "Selected Design Opportunity: None"
        )
        self.candidate_activity_title_input.clear()
        self.candidate_activity_method_input.setCurrentIndex(
            0
        )
        self.candidate_activity_phase_input.clear()
        self.candidate_activity_description_input.clear()
        self.candidate_activity_notes_input.clear()
        self.add_candidate_activity_button.setEnabled(
            False
        )

    @staticmethod
    def _opportunity_decomposition_complete(
        opportunity,
    ):
        if opportunity is None:
            return False

        return all(
            [
                opportunity.required_conditions.strip(),
                opportunity.stimulus_information.strip(),
                opportunity.response_opportunity.strip(),
                opportunity.evidence_capture_plan.strip(),
            ]
        )

    def _update_add_candidate_activity_button(
        self,
        *_,
    ):
        opportunity = self._selected_design_opportunity()

        enabled = bool(
            opportunity is not None
            and self._opportunity_decomposition_complete(
                opportunity
            )
            and self.candidate_activity_title_input.text().strip()
            and (
                self.candidate_activity_method_input.currentIndex()
                > 0
            )
            and (
                self.candidate_activity_description_input
                .toPlainText()
                .strip()
            )
        )

        self.add_candidate_activity_button.setEnabled(
            enabled
        )

    def _add_candidate_exercise_activity(self):
        opportunity = self._selected_design_opportunity()

        if not self._opportunity_decomposition_complete(
            opportunity
        ):
            QMessageBox.warning(
                self,
                "Candidate Exercise Activity",
                "Complete and save the selected Design Opportunity "
                "decomposition before creating a Candidate Exercise "
                "Activity.",
            )
            return

        activity = CandidateExerciseActivity(
            title=(
                self.candidate_activity_title_input
                .text()
                .strip()
            ),
            description=(
                self.candidate_activity_description_input
                .toPlainText()
                .strip()
            ),
            delivery_method=(
                self.candidate_activity_method_input
                .currentText()
            ),
            phase=(
                self.candidate_activity_phase_input
                .text()
                .strip()
            ),
            notes=(
                self.candidate_activity_notes_input
                .toPlainText()
                .strip()
            ),
            design_opportunity_id=opportunity.id,
            cto_id=opportunity.cto_id,
            collective_task_id=(
                opportunity.collective_task_id
            ),
            success_factor_id=(
                opportunity.success_factor_id
            ),
            metric_ids=list(
                opportunity.metric_ids
            ),
            evidence_requirement_ids=list(
                opportunity.evidence_requirement_ids
            ),
        )

        self.project.add_candidate_exercise_activity(
            activity
        )

        self.candidate_activity_title_input.clear()
        self.candidate_activity_method_input.setCurrentIndex(
            0
        )
        self.candidate_activity_phase_input.clear()
        self.candidate_activity_description_input.clear()
        self.candidate_activity_notes_input.clear()

        self._refresh_candidate_activities()
        self._update_add_candidate_activity_button()

    def _find_design_opportunity(
        self,
        opportunity_id,
    ):
        if self.project is None:
            return None

        for opportunity in self.project.exercise_design_opportunities:
            if opportunity.id == opportunity_id:
                return opportunity

        return None

    def _refresh_candidate_activities(self):
        self.candidate_activity_tree.clear()

        if self.project is None or self.cto is None:
            return

        activities = [
            activity
            for activity in self.project.candidate_exercise_activities
            if activity.cto_id == self.cto.id
        ]

        for activity in activities:
            opportunity = self._find_design_opportunity(
                activity.design_opportunity_id
            )

            if opportunity is None:
                opportunity_title = (
                    "Design Opportunity no longer found"
                )
                assurance_coverage = "Review required"
            else:
                opportunity_title = opportunity.title

                assurance_coverage = (
                    f"{len(activity.metric_ids)} metric(s), "
                    f"{len(activity.evidence_requirement_ids)} "
                    "evidence requirement(s)"
                )

            item = QTreeWidgetItem(
                [
                    activity.title,
                    opportunity_title,
                    activity.delivery_method or "-",
                    assurance_coverage,
                ]
            )

            item.setToolTip(
                0,
                activity.description,
            )

            if activity.phase:
                item.setToolTip(
                    2,
                    f"Phase / placement: {activity.phase}",
                )

            item.setData(
                0,
                Qt.ItemDataRole.UserRole,
                activity.id,
            )

            self.candidate_activity_tree.addTopLevelItem(
                item
            )

