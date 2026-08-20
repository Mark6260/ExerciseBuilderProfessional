from PySide6.QtCore import Qt, Signal
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

from core.assessment import (
    AssessmentOutcome,
    AssessmentRecord,
)


class AssessmentPanel(QWidget):
    """
    Professional assessment workspace.

    Admitted evidence is reviewed against the assured performance lineage
    carried by the related MEL/MIL promotion. Exercise Director preserves
    the judgement; it does not make the judgement itself.
    """

    assessment_recorded = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.project = None
        self._build_ui()

        self.evidence_list.currentRowChanged.connect(
            self._show_selected_evidence
        )
        self.outcome_input.currentIndexChanged.connect(
            self._update_record_button
        )
        self.assessor_input.textChanged.connect(
            self._update_record_button
        )
        self.record_button.clicked.connect(
            self._record_assessment
        )

    def _build_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # -------------------------------------------------
        # Evidence list
        # -------------------------------------------------

        left_frame = QFrame()
        left_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        left_layout = QVBoxLayout(left_frame)

        left_heading = QLabel(
            "ADMITTED EVIDENCE"
        )
        left_heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        guidance = QLabel(
            "Select admitted evidence to assess it against the assured "
            "performance requirement carried by its MEL/MIL lineage."
        )
        guidance.setWordWrap(True)

        self.evidence_list = QListWidget()

        left_layout.addWidget(left_heading)
        left_layout.addWidget(guidance)
        left_layout.addWidget(self.evidence_list)

        # -------------------------------------------------
        # Assessment detail
        # -------------------------------------------------

        right_frame = QFrame()
        right_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        right_layout = QVBoxLayout(right_frame)

        heading = QLabel(
            "ASSURED PERFORMANCE ASSESSMENT"
        )
        heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.evidence_title_label = QLabel(
            "Evidence: -"
        )
        self.evidence_title_label.setWordWrap(True)

        self.inject_label = QLabel(
            "Inject: -"
        )

        self.success_factor_label = QLabel(
            "Success Factor: -"
        )
        self.success_factor_label.setWordWrap(True)

        self.metric_label = QLabel(
            "Observable Metric: -"
        )
        self.metric_label.setWordWrap(True)

        self.evidence_requirement_label = QLabel(
            "Evidence Requirement: -"
        )
        self.evidence_requirement_label.setWordWrap(True)

        self.assessment_status_label = QLabel(
            "Assessment Status: -"
        )
        self.assessment_status_label.setWordWrap(True)
        self.assessment_status_label.setStyleSheet(
            "font-weight: bold;"
        )

        evidence_heading = QLabel(
            "EVIDENCE DESCRIPTION"
        )
        evidence_heading.setStyleSheet(
            "font-weight: bold;"
        )

        self.evidence_description = QTextEdit()
        self.evidence_description.setReadOnly(True)
        self.evidence_description.setMinimumHeight(120)

        assessment_heading = QLabel(
            "PROFESSIONAL JUDGEMENT"
        )
        assessment_heading.setStyleSheet(
            "font-weight: bold;"
        )

        self.outcome_input = QComboBox()
        self.outcome_input.addItem(
            "Select assessment outcome...",
            None,
        )
        self.outcome_input.addItem(
            AssessmentOutcome.ACHIEVED.value,
            AssessmentOutcome.ACHIEVED,
        )
        self.outcome_input.addItem(
            AssessmentOutcome.PARTIALLY_ACHIEVED.value,
            AssessmentOutcome.PARTIALLY_ACHIEVED,
        )
        self.outcome_input.addItem(
            AssessmentOutcome.NOT_ACHIEVED.value,
            AssessmentOutcome.NOT_ACHIEVED,
        )

        self.assessor_input = QLineEdit()
        self.assessor_input.setPlaceholderText(
            "Assessor name / role"
        )

        self.comments_input = QTextEdit()
        self.comments_input.setPlaceholderText(
            "Record the professional judgement and why the admitted evidence "
            "supports this outcome."
        )
        self.comments_input.setMinimumHeight(110)

        note = QLabel(
            "Exercise Director records the assessor's judgement and evidence "
            "considered. It does not determine readiness automatically."
        )
        note.setWordWrap(True)
        note.setStyleSheet(
            "font-style: italic;"
        )

        self.record_button = QPushButton(
            "RECORD ASSESSMENT"
        )
        self.record_button.setEnabled(False)

        right_layout.addWidget(heading)
        right_layout.addWidget(self.evidence_title_label)
        right_layout.addWidget(self.inject_label)
        right_layout.addWidget(self.success_factor_label)
        right_layout.addWidget(self.metric_label)
        right_layout.addWidget(
            self.evidence_requirement_label
        )
        right_layout.addWidget(
            self.assessment_status_label
        )
        right_layout.addWidget(evidence_heading)
        right_layout.addWidget(
            self.evidence_description
        )
        right_layout.addWidget(assessment_heading)
        right_layout.addWidget(self.outcome_input)
        right_layout.addWidget(self.assessor_input)
        right_layout.addWidget(self.comments_input)
        right_layout.addWidget(note)
        right_layout.addWidget(self.record_button)

        main_layout.addWidget(left_frame, 4)
        main_layout.addWidget(right_frame, 6)

    def set_project(self, project):
        self.project = project
        self.refresh_evidence()

    def refresh_evidence(self):
        self.evidence_list.clear()
        self._clear_detail()

        if self.project is None:
            return

        for evidence in self.project.evidence_records:
            title = evidence.title or "Untitled evidence"
            inject_text = (
                f"Inject {evidence.related_inject}"
                if evidence.related_inject is not None
                else "No inject"
            )

            self.evidence_list.addItem(
                f"{title} - {inject_text}"
            )

    def _selected_evidence(self):
        if self.project is None:
            return None

        row = self.evidence_list.currentRow()

        if row < 0 or row >= len(self.project.evidence_records):
            return None

        return self.project.evidence_records[row]

    def _find_promotion(self, inject_number):
        if self.project is None:
            return None

        wanted = str(inject_number)

        for promotion in getattr(
            self.project,
            "mel_mil_promotions",
            [],
        ):
            if str(promotion.inject_number) == wanted:
                return promotion

        return None

    def _find_cto(self, cto_id):
        if self.project is None:
            return None

        for cto in getattr(
            self.project,
            "collective_training_objectives",
            [],
        ):
            if cto.id == cto_id:
                return cto

        return None

    @staticmethod
    def _find_success_factor(cto, factor_id):
        if cto is None:
            return None

        for task in cto.collective_tasks:
            for factor in task.success_factors:
                if factor.id == factor_id:
                    return factor

        return None

    @staticmethod
    def _metric_texts(cto, metric_ids):
        if cto is None:
            return []

        wanted = set(metric_ids)

        return [
            metric.description
            for task in cto.collective_tasks
            for factor in task.success_factors
            for metric in factor.metrics
            if metric.id in wanted
        ]

    @staticmethod
    def _evidence_requirement_texts(
        cto,
        evidence_requirement_ids,
    ):
        if cto is None:
            return []

        wanted = set(evidence_requirement_ids)
        values = []

        for task in cto.collective_tasks:
            for factor in task.success_factors:
                for metric in factor.metrics:
                    for requirement in metric.evidence_requirements:
                        if requirement.id in wanted:
                            values.append(
                                requirement.description
                            )

        return values

    def _assessments_for_evidence(
        self,
        evidence_id,
    ):
        if self.project is None or not evidence_id:
            return []

        return [
            assessment
            for assessment in self.project.assessment_records
            if evidence_id in assessment.evidence_ids
        ]

    def _show_existing_assessment(
        self,
        assessments,
    ):
        count = len(assessments)

        if count == 1:
            assessment = assessments[0]
            self.assessment_status_label.setText(
                "Assessment Status: ASSESSMENT RECORDED"
            )
        else:
            assessment = assessments[-1]
            self.assessment_status_label.setText(
                "Assessment Status: "
                f"{count} ASSESSMENT RECORDS EXIST - REVIEW REQUIRED"
            )

        index = self.outcome_input.findData(
            assessment.outcome
        )
        if index >= 0:
            self.outcome_input.setCurrentIndex(index)

        self.assessor_input.setText(
            assessment.assessor
        )
        self.comments_input.setPlainText(
            assessment.comments
        )

        self.outcome_input.setEnabled(False)
        self.assessor_input.setReadOnly(True)
        self.comments_input.setReadOnly(True)
        self.record_button.setText(
            "ASSESSMENT RECORDED"
        )
        self.record_button.setEnabled(False)

    def _prepare_new_assessment(self):
        self.assessment_status_label.setText(
            "Assessment Status: NOT YET ASSESSED"
        )
        self.outcome_input.setEnabled(True)
        self.assessor_input.setReadOnly(False)
        self.comments_input.setReadOnly(False)
        self.outcome_input.setCurrentIndex(0)
        self.comments_input.clear()
        self.record_button.setText(
            "RECORD ASSESSMENT"
        )

    def _show_selected_evidence(self, row):
        evidence = self._selected_evidence()

        if evidence is None:
            self._clear_detail()
            return

        self.evidence_title_label.setText(
            f"Evidence: {evidence.title or '-'}"
        )
        self.inject_label.setText(
            "Inject: "
            + (
                str(evidence.related_inject)
                if evidence.related_inject is not None
                else "-"
            )
        )
        self.evidence_description.setPlainText(
            evidence.description or ""
        )

        promotion = self._find_promotion(
            evidence.related_inject
        )

        if promotion is None:
            self.success_factor_label.setText(
                "Success Factor: No assured MEL/MIL lineage found"
            )
            self.metric_label.setText(
                "Observable Metric: -"
            )
            self.evidence_requirement_label.setText(
                "Evidence Requirement: -"
            )
            assessments = self._assessments_for_evidence(
                evidence.evidence_id
            )
            if assessments:
                self._show_existing_assessment(
                    assessments
                )
            else:
                self._prepare_new_assessment()
                self._update_record_button()
            return

        cto = self._find_cto(
            promotion.cto_id
        )
        factor = self._find_success_factor(
            cto,
            promotion.success_factor_id,
        )
        metrics = self._metric_texts(
            cto,
            promotion.metric_ids,
        )
        requirements = (
            self._evidence_requirement_texts(
                cto,
                promotion.evidence_requirement_ids,
            )
        )

        self.success_factor_label.setText(
            "Success Factor: "
            + (
                factor.description
                if factor is not None
                else "Not found - review lineage"
            )
        )
        self.metric_label.setText(
            "Observable Metric: "
            + (
                " | ".join(metrics)
                if metrics
                else "Not found - review lineage"
            )
        )
        self.evidence_requirement_label.setText(
            "Evidence Requirement: "
            + (
                " | ".join(requirements)
                if requirements
                else "Not found - review lineage"
            )
        )

        assessments = self._assessments_for_evidence(
            evidence.evidence_id
        )

        if assessments:
            self._show_existing_assessment(
                assessments
            )
        else:
            self._prepare_new_assessment()
            self._update_record_button()

    def _clear_detail(self):
        if not hasattr(
            self,
            "evidence_title_label",
        ):
            return

        self.evidence_title_label.setText(
            "Evidence: -"
        )
        self.inject_label.setText(
            "Inject: -"
        )
        self.success_factor_label.setText(
            "Success Factor: -"
        )
        self.metric_label.setText(
            "Observable Metric: -"
        )
        self.evidence_requirement_label.setText(
            "Evidence Requirement: -"
        )
        self.evidence_description.clear()
        self.assessment_status_label.setText(
            "Assessment Status: -"
        )
        self.outcome_input.setEnabled(True)
        self.assessor_input.setReadOnly(False)
        self.comments_input.setReadOnly(False)
        self.outcome_input.setCurrentIndex(0)
        self.comments_input.clear()
        self.record_button.setText(
            "RECORD ASSESSMENT"
        )
        self.record_button.setEnabled(False)

    def _update_record_button(self, *_):
        evidence = self._selected_evidence()

        if evidence is None:
            self.record_button.setEnabled(False)
            return

        if self._assessments_for_evidence(
            evidence.evidence_id
        ):
            self.record_button.setEnabled(False)
            return

        promotion = self._find_promotion(
            evidence.related_inject
        )

        enabled = bool(
            promotion is not None
            and self.outcome_input.currentData() is not None
            and self.assessor_input.text().strip()
        )

        self.record_button.setEnabled(
            enabled
        )

    def _record_assessment(self):
        evidence = self._selected_evidence()

        if evidence is None:
            return

        if self._assessments_for_evidence(
            evidence.evidence_id
        ):
            self._show_existing_assessment(
                self._assessments_for_evidence(
                    evidence.evidence_id
                )
            )
            return

        promotion = self._find_promotion(
            evidence.related_inject
        )

        if promotion is None:
            return

        outcome = self.outcome_input.currentData()

        if outcome is None:
            return

        assessment = AssessmentRecord(
            inject_number=(
                evidence.related_inject
                if evidence.related_inject is not None
                else 0
            ),
            objective_title=(
                evidence.related_objective or ""
            ),
            cto_id=promotion.cto_id,
            collective_task_id=(
                promotion.collective_task_id
            ),
            success_factor_id=(
                promotion.success_factor_id
            ),
            metric_ids=list(
                promotion.metric_ids
            ),
            evidence_requirement_ids=list(
                promotion.evidence_requirement_ids
            ),
            outcome=outcome,
            evidence_ids=[
                evidence.evidence_id
            ],
            comments=(
                self.comments_input
                .toPlainText()
                .strip()
            ),
            assessor=(
                self.assessor_input
                .text()
                .strip()
            ),
        )

        assessment.mark_recorded_now()

        self.assessment_recorded.emit(
            assessment
        )

        self._show_existing_assessment(
            [assessment]
        )
