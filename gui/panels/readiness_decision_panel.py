from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.readiness.readiness_decision import (
    ReadinessDecision,
    ReadinessDecisionOutcome,
    AssessmentExceptionReason,
)


class ReadinessDecisionPanel(QWidget):
    """
    Workspace for recording an authorised readiness decision.

    Exercise Director presents the assessments and evidence available
    to the decision-maker. It does not determine readiness automatically.
    """

    readiness_decision_recorded = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.project = None

        self._build_ui()

        self.assessment_list.itemSelectionChanged.connect(
            self._show_selected_assessment
        )

        self.outcome_combo.currentIndexChanged.connect(
            self._update_record_button
        )

        self.decision_maker_edit.textChanged.connect(
            self._update_record_button
        )

        self.rationale_edit.textChanged.connect(
            self._update_record_button
        )

        self.exception_combo.currentIndexChanged.connect(
            self._update_exception_state
        )

        self.record_button.clicked.connect(
            self._record_readiness_decision
        )
        self.new_decision_button.clicked.connect(
            self._start_new_decision
        )

        self.decision_history_list.currentRowChanged.connect(
            self._show_historical_decision
        )

    def _build_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # -------------------------------------------------
        # Assessment records
        # -------------------------------------------------

        left_frame = QFrame()
        left_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        left_layout = QVBoxLayout(left_frame)

        heading = QLabel(
            "RECORDED ASSESSMENTS"
        )
        heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        guidance = QLabel(
            "Select the professional assessments that the "
            "authorised decision-maker wishes to consider."
        )
        guidance.setWordWrap(True)

        self.assessment_list = QListWidget()
        self.assessment_list.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection
        )

        left_layout.addWidget(heading)
        left_layout.addWidget(guidance)
        left_layout.addWidget(
            self.assessment_list
        )

        history_heading = QLabel(
            "AUTHORISED READINESS DECISION HISTORY"
        )
        history_heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        history_guidance = QLabel(
            "Select a recorded decision to inspect the "
            "authorised historical record."
        )
        history_guidance.setWordWrap(True)

        self.decision_history_list = QListWidget()
        self.decision_history_list.setMinimumHeight(150)

        left_layout.addWidget(history_heading)
        left_layout.addWidget(history_guidance)
        left_layout.addWidget(
            self.decision_history_list
        )

        # -------------------------------------------------
        # Readiness decision
        # -------------------------------------------------

        right_frame = QFrame()
        right_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        right_layout = QVBoxLayout(right_frame)

        decision_heading = QLabel(
            "AUTHORISED READINESS DECISION"
        )
        decision_heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        right_layout.addWidget(
            decision_heading
        )

        self.assessment_summary = QLabel(
            "Assessment: -"
        )
        self.assessment_summary.setWordWrap(True)

        right_layout.addWidget(
            self.assessment_summary
        )

        outcome_heading = QLabel(
            "READINESS OUTCOME"
        )
        outcome_heading.setStyleSheet(
            "font-weight: bold;"
        )

        right_layout.addWidget(
            outcome_heading
        )

        self.outcome_combo = QComboBox()

        self.outcome_combo.addItem(
            "Select readiness outcome...",
            None,
        )

        for outcome in ReadinessDecisionOutcome:
            if outcome == ReadinessDecisionOutcome.NOT_ASSESSED:
                continue

            self.outcome_combo.addItem(
                outcome.value,
                outcome,
            )

        right_layout.addWidget(
            self.outcome_combo
        )

        authority_heading = QLabel(
            "DECISION AUTHORITY"
        )
        authority_heading.setStyleSheet(
            "font-weight: bold;"
        )

        right_layout.addWidget(
            authority_heading
        )

        self.decision_maker_edit = QLineEdit()
        self.decision_maker_edit.setPlaceholderText(
            "Decision-maker name"
        )

        self.decision_authority_edit = QLineEdit()
        self.decision_authority_edit.setPlaceholderText(
            "Role / decision authority"
        )

        right_layout.addWidget(
            self.decision_maker_edit
        )
        right_layout.addWidget(
            self.decision_authority_edit
        )

        rationale_heading = QLabel(
            "RATIONALE"
        )
        rationale_heading.setStyleSheet(
            "font-weight: bold;"
        )

        right_layout.addWidget(
            rationale_heading
        )

        self.rationale_edit = QTextEdit()
        self.rationale_edit.setPlaceholderText(
            "Record the professional rationale for the "
            "readiness decision, including the assessments "
            "and evidence considered."
        )

        right_layout.addWidget(
            self.rationale_edit
        )

        limitations_heading = QLabel(
            "LIMITATIONS"
        )
        limitations_heading.setStyleSheet(
            "font-weight: bold;"
        )

        right_layout.addWidget(
            limitations_heading
        )

        self.limitations_edit = QTextEdit()
        self.limitations_edit.setPlaceholderText(
            "Record any limitations attached to this "
            "readiness decision."
        )

        right_layout.addWidget(
            self.limitations_edit
        )

        required_action_heading = QLabel(
            "REQUIRED ACTION"
        )
        required_action_heading.setStyleSheet(
            "font-weight: bold;"
        )

        right_layout.addWidget(
            required_action_heading
        )

        self.required_action_edit = QTextEdit()
        self.required_action_edit.setPlaceholderText(
            "Record any action required following this decision."
        )

        right_layout.addWidget(
            self.required_action_edit
        )

        # -------------------------------------------------
        # Assessment exception
        # -------------------------------------------------

        exception_heading = QLabel(
            "ASSESSMENT EXCEPTION"
        )
        exception_heading.setStyleSheet(
            "font-weight: bold;"
        )

        right_layout.addWidget(
            exception_heading
        )

        self.exception_combo = QComboBox()

        self.exception_combo.addItem(
            "No assessment exception",
            None,
        )

        for reason in AssessmentExceptionReason:
            self.exception_combo.addItem(
                reason.value,
                reason,
            )

        right_layout.addWidget(
            self.exception_combo
        )

        self.exception_explanation_edit = QTextEdit()
        self.exception_explanation_edit.setPlaceholderText(
            "Explain why the required assessment could not "
            "be completed or why an exception applies."
        )

        self.exception_explanation_edit.setEnabled(
            False
        )

        right_layout.addWidget(
            self.exception_explanation_edit
        )

        guidance_label = QLabel(
            "Exercise Director records the authorised "
            "professional judgement, the assessments considered "
            "and any limitations or exceptions. It does not "
            "determine readiness automatically."
        )

        guidance_label.setWordWrap(True)
        guidance_label.setStyleSheet(
            "font-style: italic;"
        )

        right_layout.addWidget(
            guidance_label
        )

        self.new_decision_button = QPushButton(
            "RECORD NEW DECISION"
        )
        self.new_decision_button.setVisible(False)

        self.record_button = QPushButton(
            "RECORD READINESS DECISION"
        )
        self.record_button.setEnabled(False)

        right_layout.addWidget(
            self.new_decision_button
        )
        right_layout.addWidget(
            self.record_button
        )

        main_layout.addWidget(
            left_frame,
            4,
        )

        main_layout.addWidget(
            right_frame,
            6,
        )

    def set_project(self, project):
        self.project = project
        self._reset_decision_form()
        self.refresh_assessments()
        self.refresh_decision_history()
        self._load_existing_decision()

    def refresh_decision_history(self):
        self.decision_history_list.blockSignals(True)
        self.decision_history_list.clear()

        if self.project is None:
            self.decision_history_list.blockSignals(False)
            return

        decisions = getattr(
            self.project,
            "readiness_decisions",
            [],
        )

        for decision in reversed(decisions):
            recorded_at = decision.recorded_at or "Time not recorded"
            decision_maker = (
                decision.decision_maker
                or "Decision-maker not recorded"
            )
            authority = (
                decision.decision_authority
                or "Authority not recorded"
            )

            self.decision_history_list.addItem(
                f"{recorded_at} | {decision.outcome.value} | "
                f"{decision_maker} | {authority}"
            )

        self.decision_history_list.blockSignals(False)

    def _show_historical_decision(self, row):
        if self.project is None or row < 0:
            return

        decisions = getattr(
            self.project,
            "readiness_decisions",
            [],
        )

        if not decisions:
            return

        decision_index = len(decisions) - 1 - row

        if not 0 <= decision_index < len(decisions):
            return

        decision = decisions[decision_index]
        self._display_decision(
            decision,
            historical=True,
        )

    def _display_decision(
        self,
        decision,
        historical=False,
    ):
        assessment_ids = set(
            decision.assessment_ids
        )

        assessments = getattr(
            self.project,
            "assessment_records",
            [],
        )

        self.assessment_list.blockSignals(True)
        self.assessment_list.clearSelection()

        for row, assessment in enumerate(assessments):
            if assessment.assessment_id in assessment_ids:
                item = self.assessment_list.item(row)
                if item is not None:
                    item.setSelected(True)

        self.assessment_list.blockSignals(False)

        selected = self._selected_assessments()

        if len(selected) == 1:
            assessment = selected[0]
            self.assessment_summary.setText(
                f"Assessment: {assessment.outcome.value}\\n"
                f"Inject: {assessment.inject_number}\\n"
                f"Objective: "
                f"{assessment.objective_title or '-'}\\n"
                f"Assessor: "
                f"{assessment.assessor or '-'}"
            )
        elif len(selected) > 1:
            self.assessment_summary.setText(
                f"{len(selected)} professional assessments "
                "selected for consideration."
            )
        else:
            self.assessment_summary.setText(
                "Assessment: Recorded assessment references "
                "could not be resolved."
            )

        outcome_index = self.outcome_combo.findData(
            decision.outcome
        )
        if outcome_index >= 0:
            self.outcome_combo.setCurrentIndex(
                outcome_index
            )

        self.decision_maker_edit.setText(
            decision.decision_maker
        )
        self.decision_authority_edit.setText(
            decision.decision_authority
        )
        self.rationale_edit.setPlainText(
            decision.rationale
        )
        self.limitations_edit.setPlainText(
            decision.limitations
        )
        self.required_action_edit.setPlainText(
            decision.required_action
        )

        if decision.exception_reason is None:
            self.exception_combo.setCurrentIndex(0)
        else:
            exception_index = self.exception_combo.findData(
                decision.exception_reason
            )
            if exception_index >= 0:
                self.exception_combo.setCurrentIndex(
                    exception_index
                )

        self.exception_explanation_edit.setPlainText(
            decision.exception_explanation
        )

        self._show_recorded_state(decision)

        if historical:
            self.record_button.setText(
                "HISTORICAL READINESS DECISION"
            )
            self.new_decision_button.setVisible(True)

    def _start_new_decision(self):
        if self.project is None:
            return

        self.decision_history_list.blockSignals(True)
        self.decision_history_list.clearSelection()
        self.decision_history_list.setCurrentRow(-1)
        self.decision_history_list.blockSignals(False)

        self.assessment_list.blockSignals(True)
        self.assessment_list.clearSelection()
        self.assessment_list.blockSignals(False)

        self._reset_decision_form()
        self._clear_assessment_summary()
        self.new_decision_button.setVisible(False)
        self._update_record_button()

    def _reset_decision_form(self):
        self.assessment_list.setEnabled(True)

        self.outcome_combo.setEnabled(True)
        self.outcome_combo.setCurrentIndex(0)

        self.decision_maker_edit.setReadOnly(False)
        self.decision_authority_edit.setReadOnly(False)
        self.rationale_edit.setReadOnly(False)
        self.limitations_edit.setReadOnly(False)
        self.required_action_edit.setReadOnly(False)

        self.exception_combo.setEnabled(True)
        self.exception_combo.setCurrentIndex(0)

        self.exception_explanation_edit.setReadOnly(False)
        self.exception_explanation_edit.setEnabled(False)

        self.decision_maker_edit.clear()
        self.decision_authority_edit.clear()
        self.rationale_edit.clear()
        self.limitations_edit.clear()
        self.required_action_edit.clear()
        self.exception_explanation_edit.clear()

        self.record_button.setText(
            "RECORD READINESS DECISION"
        )
        self.record_button.setEnabled(False)
        self.new_decision_button.setVisible(False)

        self._clear_assessment_summary()

    def _load_existing_decision(self):
        if self.project is None:
            return

        decisions = getattr(
            self.project,
            "readiness_decisions",
            [],
        )

        if not decisions:
            self._update_record_button()
            return

        decision = decisions[-1]
        self._display_decision(decision)

        if self.decision_history_list.count() > 0:
            self.decision_history_list.blockSignals(True)
            self.decision_history_list.setCurrentRow(0)
            self.decision_history_list.blockSignals(False)

    def refresh_assessments(self):
        self.assessment_list.clear()

        if self.project is None:
            self._clear_assessment_summary()
            return

        for assessment in getattr(
            self.project,
            "assessment_records",
            [],
        ):
            item_text = (
                f"{assessment.outcome.value}"
                f" - Inject {assessment.inject_number}"
                f" - {assessment.objective_title or 'Objective not recorded'}"
            )

            self.assessment_list.addItem(
                item_text
            )

        self._clear_assessment_summary()
        self._update_record_button()

    def _selected_assessments(self):
        if self.project is None:
            return []

        selected_rows = sorted(
            {
                self.assessment_list.row(item)
                for item in self.assessment_list.selectedItems()
            }
        )

        assessments = getattr(
            self.project,
            "assessment_records",
            [],
        )

        return [
            assessments[row]
            for row in selected_rows
            if 0 <= row < len(assessments)
        ]

    def _show_selected_assessment(self):
        selected = self._selected_assessments()

        if not selected:
            self._clear_assessment_summary()
            self._update_record_button()
            return

        if len(selected) == 1:
            assessment = selected[0]

            summary = (
                f"Assessment: {assessment.outcome.value}\n"
                f"Inject: {assessment.inject_number}\n"
                f"Objective: "
                f"{assessment.objective_title or '-'}\n"
                f"Assessor: "
                f"{assessment.assessor or '-'}"
            )

        else:
            summary = (
                f"{len(selected)} professional assessments "
                "selected for consideration."
            )

        self.assessment_summary.setText(
            summary
        )

        self._update_record_button()

    def _clear_assessment_summary(self):
        self.assessment_summary.setText(
            "Assessment: -"
        )

    def _update_exception_state(self):
        has_exception = (
            self.exception_combo.currentData()
            is not None
        )

        self.exception_explanation_edit.setEnabled(
            has_exception
        )

        if not has_exception:
            self.exception_explanation_edit.clear()

    def _update_record_button(self):
        if not hasattr(
            self,
            "record_button",
        ):
            return

        has_assessment = bool(
            self._selected_assessments()
        )

        has_outcome = (
            self.outcome_combo.currentData()
            is not None
        )

        has_decision_maker = bool(
            self.decision_maker_edit.text().strip()
        )

        has_rationale = bool(
            self.rationale_edit.toPlainText().strip()
        )

        self.record_button.setEnabled(
            has_assessment
            and has_outcome
            and has_decision_maker
            and has_rationale
        )

    def _record_readiness_decision(self):
        selected_assessments = (
            self._selected_assessments()
        )

        if not selected_assessments:
            return

        outcome = self.outcome_combo.currentData()

        if outcome is None:
            return

        decision_maker = (
            self.decision_maker_edit.text().strip()
        )

        rationale = (
            self.rationale_edit.toPlainText().strip()
        )

        if not decision_maker or not rationale:
            return

        decision = ReadinessDecision()

        decision.outcome = outcome
        decision.decision_maker = decision_maker

        decision.decision_authority = (
            self.decision_authority_edit.text().strip()
        )

        decision.rationale = rationale

        decision.limitations = (
            self.limitations_edit.toPlainText().strip()
        )

        decision.required_action = (
            self.required_action_edit.toPlainText().strip()
        )

        decision.exception_reason = (
            self.exception_combo.currentData()
        )

        decision.exception_explanation = (
            self.exception_explanation_edit
            .toPlainText()
            .strip()
        )

        for assessment in selected_assessments:
            decision.add_assessment_id(
                assessment.assessment_id
            )

        decision.mark_recorded_now()

        self.readiness_decision_recorded.emit(
            decision
        )

        self.refresh_decision_history()

        self._show_recorded_state(
            decision
        )

        if self.decision_history_list.count() > 0:
            self.decision_history_list.blockSignals(True)
            self.decision_history_list.setCurrentRow(0)
            self.decision_history_list.blockSignals(False)

    def _show_recorded_state(
        self,
        decision,
    ):
        self.outcome_combo.setEnabled(False)
        self.decision_maker_edit.setReadOnly(True)
        self.decision_authority_edit.setReadOnly(True)
        self.rationale_edit.setReadOnly(True)
        self.limitations_edit.setReadOnly(True)
        self.required_action_edit.setReadOnly(True)

        self.exception_combo.setEnabled(False)
        self.exception_explanation_edit.setReadOnly(
            True
        )

        self.assessment_list.setEnabled(False)

        self.record_button.setText(
            "READINESS DECISION RECORDED"
        )
        self.record_button.setEnabled(False)
        self.new_decision_button.setVisible(True)