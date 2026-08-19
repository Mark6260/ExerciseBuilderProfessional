from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
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
from core.candidate_mel_mil_activity import CandidateMelMilActivity
from core.inject import Inject
from core.mel_mil_promotion import MelMilPromotion


class ExerciseDesignPanel(QWidget):
    inject_promoted = Signal(int)

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

        opportunity_manage_layout = QHBoxLayout()

        self.edit_opportunity_button = QPushButton(
            "EDIT SELECTED OPPORTUNITY"
        )
        self.edit_opportunity_button.setEnabled(
            False
        )
        self.edit_opportunity_button.clicked.connect(
            self._edit_selected_design_opportunity
        )

        self.delete_opportunity_button = QPushButton(
            "DELETE SELECTED OPPORTUNITY"
        )
        self.delete_opportunity_button.setEnabled(
            False
        )
        self.delete_opportunity_button.clicked.connect(
            self._delete_selected_design_opportunity
        )

        opportunity_manage_layout.addStretch()
        opportunity_manage_layout.addWidget(
            self.edit_opportunity_button
        )
        opportunity_manage_layout.addWidget(
            self.delete_opportunity_button
        )

        opportunity_layout.addLayout(
            opportunity_manage_layout
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

        activity_manage_layout = QHBoxLayout()

        self.edit_candidate_activity_button = QPushButton(
            "EDIT SELECTED ACTIVITY"
        )
        self.edit_candidate_activity_button.setEnabled(
            False
        )
        self.edit_candidate_activity_button.clicked.connect(
            self._edit_selected_candidate_activity
        )

        self.delete_candidate_activity_button = QPushButton(
            "DELETE SELECTED ACTIVITY"
        )
        self.delete_candidate_activity_button.setEnabled(
            False
        )
        self.delete_candidate_activity_button.clicked.connect(
            self._delete_selected_candidate_activity
        )

        activity_manage_layout.addStretch()
        activity_manage_layout.addWidget(
            self.edit_candidate_activity_button
        )
        activity_manage_layout.addWidget(
            self.delete_candidate_activity_button
        )

        activity_layout.addLayout(
            activity_manage_layout
        )

        self.candidate_activity_tree.itemSelectionChanged.connect(
            self._candidate_activity_selected
        )

        layout.addWidget(
            activity_frame
        )

        # -------------------------------------------------
        # Candidate MEL/MIL Activity
        # -------------------------------------------------

        mel_frame = QFrame()
        mel_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )
        mel_layout = QVBoxLayout(
            mel_frame
        )

        mel_title = QLabel(
            "CANDIDATE MEL/MIL ACTIVITY"
        )
        mel_title.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        mel_layout.addWidget(
            mel_title
        )

        mel_guidance = QLabel(
            "Select a Candidate Exercise Activity above, then define a "
            "candidate MEL/MIL-level event or control activity that could "
            "deliver it. This is still a design object — do not write the "
            "final inject wording here."
        )
        mel_guidance.setWordWrap(
            True
        )
        mel_layout.addWidget(
            mel_guidance
        )

        self.selected_mel_parent_label = QLabel(
            "Selected Candidate Exercise Activity: None"
        )
        self.selected_mel_parent_label.setWordWrap(
            True
        )
        mel_layout.addWidget(
            self.selected_mel_parent_label
        )

        self.mel_title_input = QLineEdit()
        self.mel_title_input.setPlaceholderText(
            "e.g. Competing incident reports reach HQ"
        )
        mel_layout.addWidget(
            self.mel_title_input
        )

        self.mel_type_input = QComboBox()
        self.mel_type_input.addItems(
            [
                "Select MEL/MIL activity type...",
                "Scenario event",
                "Information release",
                "Control-cell action",
                "Role-play interaction",
                "Decision point",
                "Live activity",
                "Background activity",
                "Other",
            ]
        )
        mel_layout.addWidget(
            self.mel_type_input
        )

        mel_position_layout = QHBoxLayout()

        self.mel_phase_input = QLineEdit()
        self.mel_phase_input.setPlaceholderText(
            "Phase / placement"
        )

        self.mel_timing_input = QLineEdit()
        self.mel_timing_input.setPlaceholderText(
            "Timing / window, e.g. 09:15-09:30"
        )

        mel_position_layout.addWidget(
            self.mel_phase_input
        )
        mel_position_layout.addWidget(
            self.mel_timing_input
        )

        mel_layout.addLayout(
            mel_position_layout
        )

        self.mel_event_summary_input = QTextEdit()
        self.mel_event_summary_input.setPlaceholderText(
            "Describe what happens at MEL/MIL level: the event, release, "
            "interaction or control action. Do not write final inject text."
        )
        self.mel_event_summary_input.setFixedHeight(
            80
        )
        mel_layout.addWidget(
            self.mel_event_summary_input
        )

        self.mel_intended_effect_input = QTextEdit()
        self.mel_intended_effect_input.setPlaceholderText(
            "What opportunity should this activity create for the training "
            "audience to respond, decide, coordinate or produce evidence?"
        )
        self.mel_intended_effect_input.setFixedHeight(
            70
        )
        mel_layout.addWidget(
            self.mel_intended_effect_input
        )

        self.mel_control_notes_input = QTextEdit()
        self.mel_control_notes_input.setPlaceholderText(
            "Control notes (optional) — dependencies, sequencing, realism "
            "or ExCon considerations."
        )
        self.mel_control_notes_input.setFixedHeight(
            60
        )
        mel_layout.addWidget(
            self.mel_control_notes_input
        )

        self.add_mel_activity_button = QPushButton(
            "ADD CANDIDATE MEL/MIL ACTIVITY"
        )
        self.add_mel_activity_button.setEnabled(
            False
        )
        self.add_mel_activity_button.clicked.connect(
            self._add_candidate_mel_mil_activity
        )
        mel_layout.addWidget(
            self.add_mel_activity_button
        )

        self.mel_activity_tree = QTreeWidget()
        self.mel_activity_tree.setColumnCount(
            6
        )
        self.mel_activity_tree.setHeaderLabels(
            [
                "Candidate MEL/MIL Activity",
                "Parent Exercise Activity",
                "Type",
                "Phase / Timing",
                "Assurance Coverage",
                "Workspace Status",
            ]
        )
        self.mel_activity_tree.setMinimumHeight(
            160
        )
        self.mel_activity_tree.header().setStretchLastSection(
            True
        )
        self.mel_activity_tree.setColumnWidth(
            0,
            300,
        )
        self.mel_activity_tree.setColumnWidth(
            1,
            340,
        )
        self.mel_activity_tree.setColumnWidth(
            2,
            190,
        )
        self.mel_activity_tree.setColumnWidth(
            3,
            220,
        )

        mel_layout.addWidget(
            self.mel_activity_tree
        )

        mel_manage_layout = QHBoxLayout()

        self.edit_mel_activity_button = QPushButton(
            "EDIT SELECTED MEL/MIL ACTIVITY"
        )
        self.edit_mel_activity_button.setEnabled(
            False
        )
        self.edit_mel_activity_button.clicked.connect(
            self._edit_selected_mel_activity
        )

        self.promote_mel_activity_button = QPushButton(
            "PROMOTE TO MEL/MIL DRAFT"
        )
        self.promote_mel_activity_button.setEnabled(
            False
        )
        self.promote_mel_activity_button.clicked.connect(
            self._promote_selected_mel_activity
        )

        self.delete_mel_activity_button = QPushButton(
            "DELETE SELECTED MEL/MIL ACTIVITY"
        )
        self.delete_mel_activity_button.setEnabled(
            False
        )
        self.delete_mel_activity_button.clicked.connect(
            self._delete_selected_mel_activity
        )

        mel_manage_layout.addStretch()
        mel_manage_layout.addWidget(
            self.promote_mel_activity_button
        )
        mel_manage_layout.addWidget(
            self.edit_mel_activity_button
        )
        mel_manage_layout.addWidget(
            self.delete_mel_activity_button
        )

        mel_layout.addLayout(
            mel_manage_layout
        )

        self.mel_activity_tree.itemSelectionChanged.connect(
            self._mel_activity_selected
        )

        self.mel_title_input.textChanged.connect(
            self._update_add_mel_activity_button
        )
        self.mel_type_input.currentIndexChanged.connect(
            self._update_add_mel_activity_button
        )
        self.mel_event_summary_input.textChanged.connect(
            self._update_add_mel_activity_button
        )
        self.mel_intended_effect_input.textChanged.connect(
            self._update_add_mel_activity_button
        )

        layout.addWidget(
            mel_frame
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
        self.mel_activity_tree.clear()
        self._clear_mel_activity_editor()
        if hasattr(
            self,
            "edit_opportunity_button",
        ):
            self.edit_opportunity_button.setEnabled(
                False
            )
            self.delete_opportunity_button.setEnabled(
                False
            )
            self.edit_candidate_activity_button.setEnabled(
                False
            )
            self.delete_candidate_activity_button.setEnabled(
                False
            )
            self.edit_mel_activity_button.setEnabled(
                False
            )
            self.delete_mel_activity_button.setEnabled(
                False
            )
            self.promote_mel_activity_button.setEnabled(
                False
            )
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
        self._refresh_mel_activities()

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

        self.edit_opportunity_button.setEnabled(
            opportunity is not None
        )
        self.delete_opportunity_button.setEnabled(
            opportunity is not None
        )

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

    def _select_design_opportunity_by_id(
        self,
        opportunity_id,
    ):
        for index in range(
            self.opportunity_tree.topLevelItemCount()
        ):
            item = self.opportunity_tree.topLevelItem(
                index
            )
            if item.data(
                0,
                Qt.ItemDataRole.UserRole,
            ) == opportunity_id:
                self.opportunity_tree.setCurrentItem(
                    item
                )
                return

    def _edit_selected_design_opportunity(self):
        opportunity = self._selected_design_opportunity()

        if opportunity is None:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(
            "Edit Design Opportunity"
        )
        dialog.resize(
            680,
            420,
        )

        dialog_layout = QVBoxLayout(
            dialog
        )
        form = QFormLayout()

        title_input = QLineEdit(
            opportunity.title
        )

        description_input = QTextEdit()
        description_input.setPlainText(
            opportunity.description
        )
        description_input.setMinimumHeight(
            180
        )

        form.addRow(
            "Title:",
            title_input,
        )
        form.addRow(
            "Description:",
            description_input,
        )

        link_label = QLabel(
            "Assurance linkage is protected. Editing this opportunity "
            "does not change its CTO, Task, Success Factor, Metric or "
            "Evidence Requirement references."
        )
        link_label.setWordWrap(
            True
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(
            dialog.accept
        )
        buttons.rejected.connect(
            dialog.reject
        )

        dialog_layout.addLayout(
            form
        )
        dialog_layout.addWidget(
            link_label
        )
        dialog_layout.addWidget(
            buttons
        )

        if (
            dialog.exec()
            != QDialog.DialogCode.Accepted
        ):
            return

        title = title_input.text().strip()
        description = (
            description_input
            .toPlainText()
            .strip()
        )

        if not title or not description:
            QMessageBox.warning(
                self,
                "Edit Design Opportunity",
                "Title and description are both required.",
            )
            return

        opportunity.title = title
        opportunity.description = description

        opportunity_id = opportunity.id

        self._refresh_design_opportunities()
        self._refresh_candidate_activities()
        self._select_design_opportunity_by_id(
            opportunity_id
        )

    def _delete_selected_design_opportunity(self):
        opportunity = self._selected_design_opportunity()

        if opportunity is None:
            return

        dependent_activities = [
            activity
            for activity
            in self.project.candidate_exercise_activities
            if (
                activity.design_opportunity_id
                == opportunity.id
            )
        ]

        if dependent_activities:
            names = "\n".join(
                f"• {activity.title}"
                for activity in dependent_activities
            )

            QMessageBox.warning(
                self,
                "Delete Design Opportunity",
                "This Design Opportunity cannot be deleted because "
                "Candidate Exercise Activities depend on it:\n\n"
                f"{names}\n\n"
                "Delete or rework the dependent activities first.",
            )
            return

        answer = QMessageBox.question(
            self,
            "Delete Design Opportunity",
            (
                "Delete the selected Design Opportunity?\n\n"
                f"{opportunity.title}\n\n"
                "Its assured CTO linkage will not be altered."
            ),
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
            ),
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        self.project.exercise_design_opportunities = [
            item
            for item in self.project.exercise_design_opportunities
            if item.id != opportunity.id
        ]

        self._clear_decomposition_editor()
        self._clear_candidate_activity_editor()
        self._refresh_design_opportunities()
        self._refresh_candidate_activities()

    def _selected_candidate_activity(self):
        if self.project is None:
            return None

        items = self.candidate_activity_tree.selectedItems()

        if not items:
            return None

        activity_id = items[0].data(
            0,
            Qt.ItemDataRole.UserRole,
        )

        for activity in self.project.candidate_exercise_activities:
            if activity.id == activity_id:
                return activity

        return None

    def _candidate_activity_selected(self):
        activity = self._selected_candidate_activity()

        self.edit_candidate_activity_button.setEnabled(
            activity is not None
        )
        self.delete_candidate_activity_button.setEnabled(
            activity is not None
        )

        if activity is None:
            self.selected_mel_parent_label.setText(
                "Selected Candidate Exercise Activity: None"
            )
        else:
            self.selected_mel_parent_label.setText(
                "Selected Candidate Exercise Activity: "
                + activity.title
            )

        self._update_add_mel_activity_button()

    def _select_candidate_activity_by_id(
        self,
        activity_id,
    ):
        for index in range(
            self.candidate_activity_tree.topLevelItemCount()
        ):
            item = self.candidate_activity_tree.topLevelItem(
                index
            )
            if item.data(
                0,
                Qt.ItemDataRole.UserRole,
            ) == activity_id:
                self.candidate_activity_tree.setCurrentItem(
                    item
                )
                return

    def _edit_selected_candidate_activity(self):
        activity = self._selected_candidate_activity()

        if activity is None:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(
            "Edit Candidate Exercise Activity"
        )
        dialog.resize(
            720,
            560,
        )

        dialog_layout = QVBoxLayout(
            dialog
        )
        form = QFormLayout()

        title_input = QLineEdit(
            activity.title
        )

        method_input = QComboBox()
        method_input.addItems(
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

        method_index = method_input.findText(
            activity.delivery_method
        )
        if method_index >= 0:
            method_input.setCurrentIndex(
                method_index
            )

        phase_input = QLineEdit(
            activity.phase
        )

        description_input = QTextEdit()
        description_input.setPlainText(
            activity.description
        )
        description_input.setMinimumHeight(
            150
        )

        notes_input = QTextEdit()
        notes_input.setPlainText(
            activity.notes
        )
        notes_input.setMinimumHeight(
            100
        )

        form.addRow(
            "Title:",
            title_input,
        )
        form.addRow(
            "Delivery method:",
            method_input,
        )
        form.addRow(
            "Phase / placement:",
            phase_input,
        )
        form.addRow(
            "Description:",
            description_input,
        )
        form.addRow(
            "Designer notes:",
            notes_input,
        )

        protected_label = QLabel(
            "Parent Design Opportunity and assurance lineage are "
            "protected during editing."
        )
        protected_label.setWordWrap(
            True
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(
            dialog.accept
        )
        buttons.rejected.connect(
            dialog.reject
        )

        dialog_layout.addLayout(
            form
        )
        dialog_layout.addWidget(
            protected_label
        )
        dialog_layout.addWidget(
            buttons
        )

        if (
            dialog.exec()
            != QDialog.DialogCode.Accepted
        ):
            return

        title = title_input.text().strip()
        description = (
            description_input
            .toPlainText()
            .strip()
        )

        if (
            not title
            or not description
            or method_input.currentIndex() == 0
        ):
            QMessageBox.warning(
                self,
                "Edit Candidate Exercise Activity",
                "Title, delivery method and description are required.",
            )
            return

        activity.title = title
        activity.delivery_method = (
            method_input.currentText()
        )
        activity.phase = (
            phase_input.text().strip()
        )
        activity.description = description
        activity.notes = (
            notes_input
            .toPlainText()
            .strip()
        )

        activity_id = activity.id

        self._refresh_candidate_activities()
        self._select_candidate_activity_by_id(
            activity_id
        )

    def _delete_selected_candidate_activity(self):
        activity = self._selected_candidate_activity()

        if activity is None:
            return

        dependent_mel_activities = [
            item
            for item in self.project.candidate_mel_mil_activities
            if item.candidate_activity_id == activity.id
        ]

        if dependent_mel_activities:
            names = "\n".join(
                f"• {item.title}"
                for item in dependent_mel_activities
            )

            QMessageBox.warning(
                self,
                "Delete Candidate Exercise Activity",
                "This Candidate Exercise Activity cannot be deleted because "
                "Candidate MEL/MIL Activities depend on it:\n\n"
                f"{names}\n\n"
                "Delete or rework the dependent MEL/MIL activities first.",
            )
            return

        opportunity = self._find_design_opportunity(
            activity.design_opportunity_id
        )

        parent_title = (
            opportunity.title
            if opportunity is not None
            else "Unknown Design Opportunity"
        )

        answer = QMessageBox.question(
            self,
            "Delete Candidate Exercise Activity",
            (
                "Delete the selected Candidate Exercise Activity?\n\n"
                f"{activity.title}\n\n"
                f"Parent Design Opportunity: {parent_title}\n\n"
                "The parent Design Opportunity and assured CTO "
                "will remain unchanged."
            ),
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
            ),
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        self.project.candidate_exercise_activities = [
            item
            for item in self.project.candidate_exercise_activities
            if item.id != activity.id
        ]

        self._refresh_candidate_activities()
        self.edit_candidate_activity_button.setEnabled(
            False
        )
        self.delete_candidate_activity_button.setEnabled(
            False
        )

    def _clear_mel_activity_editor(self):
        if not hasattr(
            self,
            "selected_mel_parent_label",
        ):
            return

        self.selected_mel_parent_label.setText(
            "Selected Candidate Exercise Activity: None"
        )
        self.mel_title_input.clear()
        self.mel_type_input.setCurrentIndex(
            0
        )
        self.mel_phase_input.clear()
        self.mel_timing_input.clear()
        self.mel_event_summary_input.clear()
        self.mel_intended_effect_input.clear()
        self.mel_control_notes_input.clear()
        self.add_mel_activity_button.setEnabled(
            False
        )

    def _update_add_mel_activity_button(
        self,
        *_,
    ):
        activity = self._selected_candidate_activity()

        enabled = bool(
            activity is not None
            and self.mel_title_input.text().strip()
            and self.mel_type_input.currentIndex() > 0
            and (
                self.mel_event_summary_input
                .toPlainText()
                .strip()
            )
            and (
                self.mel_intended_effect_input
                .toPlainText()
                .strip()
            )
        )

        self.add_mel_activity_button.setEnabled(
            enabled
        )

    def _add_candidate_mel_mil_activity(self):
        parent = self._selected_candidate_activity()

        if parent is None:
            return

        activity = CandidateMelMilActivity(
            title=self.mel_title_input.text().strip(),
            activity_type=self.mel_type_input.currentText(),
            phase=self.mel_phase_input.text().strip(),
            timing_window=self.mel_timing_input.text().strip(),
            event_summary=(
                self.mel_event_summary_input
                .toPlainText()
                .strip()
            ),
            intended_effect=(
                self.mel_intended_effect_input
                .toPlainText()
                .strip()
            ),
            control_notes=(
                self.mel_control_notes_input
                .toPlainText()
                .strip()
            ),
            candidate_activity_id=parent.id,
            design_opportunity_id=parent.design_opportunity_id,
            cto_id=parent.cto_id,
            collective_task_id=parent.collective_task_id,
            success_factor_id=parent.success_factor_id,
            metric_ids=list(parent.metric_ids),
            evidence_requirement_ids=list(
                parent.evidence_requirement_ids
            ),
        )

        self.project.add_candidate_mel_mil_activity(
            activity
        )

        self.mel_title_input.clear()
        self.mel_type_input.setCurrentIndex(
            0
        )
        self.mel_phase_input.clear()
        self.mel_timing_input.clear()
        self.mel_event_summary_input.clear()
        self.mel_intended_effect_input.clear()
        self.mel_control_notes_input.clear()

        self._refresh_mel_activities()
        self._update_add_mel_activity_button()

    def _find_candidate_exercise_activity(
        self,
        activity_id,
    ):
        if self.project is None:
            return None

        for activity in self.project.candidate_exercise_activities:
            if activity.id == activity_id:
                return activity

        return None

    def _refresh_mel_activities(self):
        self.mel_activity_tree.clear()

        if self.project is None or self.cto is None:
            return

        activities = [
            activity
            for activity in self.project.candidate_mel_mil_activities
            if activity.cto_id == self.cto.id
        ]

        for activity in activities:
            parent = self._find_candidate_exercise_activity(
                activity.candidate_activity_id
            )

            if parent is None:
                parent_title = (
                    "Candidate Exercise Activity no longer found"
                )
                assurance_coverage = "Review required"
            else:
                parent_title = parent.title
                assurance_coverage = (
                    f"{len(activity.metric_ids)} metric(s), "
                    f"{len(activity.evidence_requirement_ids)} "
                    "evidence requirement(s)"
                )

            phase_timing = " / ".join(
                item
                for item in [
                    activity.phase.strip(),
                    activity.timing_window.strip(),
                ]
                if item
            ) or "-"

            promotion = self._promotion_for_mel_activity(
                activity.id
            )

            workspace_status = (
                f"MEL/MIL Draft #{promotion.inject_number}"
                if promotion is not None
                else "Candidate only"
            )

            item = QTreeWidgetItem(
                [
                    activity.title,
                    parent_title,
                    activity.activity_type or "-",
                    phase_timing,
                    assurance_coverage,
                    workspace_status,
                ]
            )
            item.setToolTip(
                0,
                activity.event_summary
            )
            item.setToolTip(
                3,
                activity.intended_effect
            )
            item.setData(
                0,
                Qt.ItemDataRole.UserRole,
                activity.id,
            )

            self.mel_activity_tree.addTopLevelItem(
                item
            )

    def _selected_mel_activity(self):
        if self.project is None:
            return None

        items = self.mel_activity_tree.selectedItems()

        if not items:
            return None

        activity_id = items[0].data(
            0,
            Qt.ItemDataRole.UserRole,
        )

        for activity in self.project.candidate_mel_mil_activities:
            if activity.id == activity_id:
                return activity

        return None

    def _mel_activity_selected(self):
        activity = self._selected_mel_activity()

        self.edit_mel_activity_button.setEnabled(
            activity is not None
        )
        self.delete_mel_activity_button.setEnabled(
            activity is not None
        )

        already_promoted = bool(
            activity is not None
            and self._promotion_for_mel_activity(
                activity.id
            )
        )

        self.promote_mel_activity_button.setEnabled(
            activity is not None
            and not already_promoted
        )

    def _select_mel_activity_by_id(
        self,
        activity_id,
    ):
        for index in range(
            self.mel_activity_tree.topLevelItemCount()
        ):
            item = self.mel_activity_tree.topLevelItem(
                index
            )
            if item.data(
                0,
                Qt.ItemDataRole.UserRole,
            ) == activity_id:
                self.mel_activity_tree.setCurrentItem(
                    item
                )
                return

    def _edit_selected_mel_activity(self):
        activity = self._selected_mel_activity()

        if activity is None:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(
            "Edit Candidate MEL/MIL Activity"
        )
        dialog.resize(
            760,
            650,
        )

        dialog_layout = QVBoxLayout(
            dialog
        )
        form = QFormLayout()

        title_input = QLineEdit(
            activity.title
        )

        type_input = QComboBox()
        type_input.addItems(
            [
                "Select MEL/MIL activity type...",
                "Scenario event",
                "Information release",
                "Control-cell action",
                "Role-play interaction",
                "Decision point",
                "Live activity",
                "Background activity",
                "Other",
            ]
        )
        type_index = type_input.findText(
            activity.activity_type
        )
        if type_index >= 0:
            type_input.setCurrentIndex(
                type_index
            )

        phase_input = QLineEdit(
            activity.phase
        )
        timing_input = QLineEdit(
            activity.timing_window
        )

        summary_input = QTextEdit()
        summary_input.setPlainText(
            activity.event_summary
        )
        summary_input.setMinimumHeight(
            130
        )

        effect_input = QTextEdit()
        effect_input.setPlainText(
            activity.intended_effect
        )
        effect_input.setMinimumHeight(
            110
        )

        notes_input = QTextEdit()
        notes_input.setPlainText(
            activity.control_notes
        )
        notes_input.setMinimumHeight(
            90
        )

        form.addRow(
            "Title:",
            title_input,
        )
        form.addRow(
            "Activity type:",
            type_input,
        )
        form.addRow(
            "Phase:",
            phase_input,
        )
        form.addRow(
            "Timing / window:",
            timing_input,
        )
        form.addRow(
            "Event summary:",
            summary_input,
        )
        form.addRow(
            "Intended effect:",
            effect_input,
        )
        form.addRow(
            "Control notes:",
            notes_input,
        )

        protected_label = QLabel(
            "Parent Candidate Exercise Activity and all upstream assurance "
            "lineage are protected during editing."
        )
        protected_label.setWordWrap(
            True
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(
            dialog.accept
        )
        buttons.rejected.connect(
            dialog.reject
        )

        dialog_layout.addLayout(
            form
        )
        dialog_layout.addWidget(
            protected_label
        )
        dialog_layout.addWidget(
            buttons
        )

        if (
            dialog.exec()
            != QDialog.DialogCode.Accepted
        ):
            return

        title = title_input.text().strip()
        summary = summary_input.toPlainText().strip()
        effect = effect_input.toPlainText().strip()

        if (
            not title
            or type_input.currentIndex() == 0
            or not summary
            or not effect
        ):
            QMessageBox.warning(
                self,
                "Edit Candidate MEL/MIL Activity",
                "Title, activity type, event summary and intended effect "
                "are required.",
            )
            return

        activity.title = title
        activity.activity_type = type_input.currentText()
        activity.phase = phase_input.text().strip()
        activity.timing_window = timing_input.text().strip()
        activity.event_summary = summary
        activity.intended_effect = effect
        activity.control_notes = (
            notes_input.toPlainText().strip()
        )

        activity_id = activity.id

        self._refresh_mel_activities()
        self._select_mel_activity_by_id(
            activity_id
        )

    def _delete_selected_mel_activity(self):
        activity = self._selected_mel_activity()

        if activity is None:
            return

        promotion = self._promotion_for_mel_activity(
            activity.id
        )

        if promotion is not None:
            QMessageBox.warning(
                self,
                "Delete Candidate MEL/MIL Activity",
                "This Candidate MEL/MIL Activity has already been promoted "
                "into the live MEL/MIL workspace as "
                f"Draft #{promotion.inject_number}.\n\n"
                "The promoted workspace row must be dealt with before its "
                "design source can be removed.",
            )
            return

        parent = self._find_candidate_exercise_activity(
            activity.candidate_activity_id
        )

        parent_title = (
            parent.title
            if parent is not None
            else "Unknown Candidate Exercise Activity"
        )

        answer = QMessageBox.question(
            self,
            "Delete Candidate MEL/MIL Activity",
            (
                "Delete the selected Candidate MEL/MIL Activity?\\n\\n"
                f"{activity.title}\\n\\n"
                f"Parent Candidate Exercise Activity: {parent_title}\\n\\n"
                "The parent activity and assured design chain will remain "
                "unchanged."
            ),
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
            ),
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        self.project.candidate_mel_mil_activities = [
            item
            for item in self.project.candidate_mel_mil_activities
            if item.id != activity.id
        ]

        self._refresh_mel_activities()
        self.edit_mel_activity_button.setEnabled(
            False
        )
        self.delete_mel_activity_button.setEnabled(
            False
        )

    def _promotion_for_mel_activity(
        self,
        candidate_mel_mil_activity_id,
    ):
        if self.project is None:
            return None

        for promotion in self.project.mel_mil_promotions:
            if (
                promotion.candidate_mel_mil_activity_id
                == candidate_mel_mil_activity_id
            ):
                return promotion

        return None

    def _next_inject_number(self):
        if not self.project.injects:
            return 1

        return (
            max(
                inject.number
                for inject in self.project.injects
            )
            + 1
        )

    def _promote_selected_mel_activity(self):
        activity = self._selected_mel_activity()

        if activity is None:
            return

        existing = self._promotion_for_mel_activity(
            activity.id
        )

        if existing is not None:
            QMessageBox.information(
                self,
                "Promote to MEL/MIL Draft",
                (
                    "This Candidate MEL/MIL Activity is already represented "
                    f"in the workspace as Draft #{existing.inject_number}."
                ),
            )
            return

        inject_number = self._next_inject_number()

        draft_inject = Inject(
            number=inject_number,
            title=activity.title,
            exercise_time=activity.timing_window,
            phase=activity.phase,
            source="Exercise Design",
            method=activity.activity_type,
            audience="",
            category="Assured Design Draft",
            inject_text=activity.event_summary,
            expected_action=activity.intended_effect,
            facilitator_notes=activity.control_notes,
            attachments=[],
        )

        promotion = MelMilPromotion(
            inject_number=inject_number,
            candidate_mel_mil_activity_id=activity.id,
            candidate_activity_id=activity.candidate_activity_id,
            design_opportunity_id=activity.design_opportunity_id,
            cto_id=activity.cto_id,
            collective_task_id=activity.collective_task_id,
            success_factor_id=activity.success_factor_id,
            metric_ids=list(activity.metric_ids),
            evidence_requirement_ids=list(
                activity.evidence_requirement_ids
            ),
        )

        self.project.add_inject(
            draft_inject
        )
        self.project.add_mel_mil_promotion(
            promotion
        )

        self._refresh_mel_activities()
        self._select_mel_activity_by_id(
            activity.id
        )

        self.inject_promoted.emit(
            inject_number
        )

        QMessageBox.information(
            self,
            "Promoted to MEL/MIL Draft",
            (
                f"Draft #{inject_number} has been added to the Exercise "
                "Workspace.\\n\\n"
                "Its design and assurance lineage has been retained."
            ),
        )

