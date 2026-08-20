from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.improvement.finding import Finding, FindingType


class FindingsPanel(QWidget):
    """
    Findings workspace.

    Records what has been identified through exercise learning and
    preserves its provenance. A finding does not prescribe or authorise
    an action.
    """

    finding_recorded = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.project = None
        self._selected_finding = None

        self._build_ui()

        self.findings_list.currentRowChanged.connect(
            self._show_selected_finding
        )
        self.title_input.textChanged.connect(
            self._update_record_button
        )
        self.description_input.textChanged.connect(
            self._update_record_button
        )
        self.recorded_by_input.textChanged.connect(
            self._update_record_button
        )
        self.record_button.clicked.connect(
            self._record_finding
        )
        self.new_button.clicked.connect(
            self._prepare_new_finding
        )

    def _build_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # -------------------------------------------------
        # Recorded findings
        # -------------------------------------------------

        left_frame = QFrame()
        left_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )
        left_layout = QVBoxLayout(left_frame)

        left_heading = QLabel("RECORDED FINDINGS")
        left_heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        guidance = QLabel(
            "Findings record what has been identified through the "
            "exercise. Select a finding to inspect its immutable record."
        )
        guidance.setWordWrap(True)

        self.findings_list = QListWidget()

        self.new_button = QPushButton("NEW FINDING")

        left_layout.addWidget(left_heading)
        left_layout.addWidget(guidance)
        left_layout.addWidget(self.findings_list)
        left_layout.addWidget(self.new_button)

        # -------------------------------------------------
        # Finding detail / creation
        # -------------------------------------------------

        right_frame = QFrame()
        right_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )
        right_layout = QVBoxLayout(right_frame)

        heading = QLabel("FINDING REVIEW")
        heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.status_label = QLabel(
            "Finding Status: NEW FINDING"
        )
        self.status_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Finding title")

        self.type_input = QComboBox()
        for finding_type in FindingType:
            self.type_input.addItem(
                finding_type.value,
                finding_type,
            )

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText(
            "Record what was identified. Do not prescribe an action here."
        )
        self.description_input.setMinimumHeight(120)

        self.recorded_by_input = QLineEdit()
        self.recorded_by_input.setPlaceholderText(
            "Recorded by - name / role"
        )

        provenance_heading = QLabel("RELATED ASSURANCE RECORDS")
        provenance_heading.setStyleSheet(
            "font-weight: bold;"
        )

        provenance_note = QLabel(
            "Select the records that support or gave rise to this finding. "
            "Links preserve provenance; they do not determine the finding."
        )
        provenance_note.setWordWrap(True)

        self.decision_combo = QComboBox()
        self.decision_combo.addItem(
            "No related readiness decision",
            "",
        )

        evidence_label = QLabel("Related Evidence")
        self.evidence_list = QListWidget()
        self.evidence_list.setSelectionMode(
            QListWidget.SelectionMode.NoSelection
        )
        self.evidence_list.setMinimumHeight(90)

        assessment_label = QLabel("Related Assessments")
        self.assessment_list = QListWidget()
        self.assessment_list.setSelectionMode(
            QListWidget.SelectionMode.NoSelection
        )
        self.assessment_list.setMinimumHeight(90)

        note = QLabel(
            "Exercise Director records the finding and its provenance. "
            "A finding does not itself create a recommendation or "
            "authorise an improvement action."
        )
        note.setWordWrap(True)
        note.setStyleSheet("font-style: italic;")

        self.record_button = QPushButton("RECORD FINDING")
        self.record_button.setEnabled(False)

        right_layout.addWidget(heading)
        right_layout.addWidget(self.status_label)
        right_layout.addWidget(QLabel("Title"))
        right_layout.addWidget(self.title_input)
        right_layout.addWidget(QLabel("Finding Type"))
        right_layout.addWidget(self.type_input)
        right_layout.addWidget(QLabel("Description"))
        right_layout.addWidget(self.description_input)
        right_layout.addWidget(QLabel("Recorded By"))
        right_layout.addWidget(self.recorded_by_input)
        right_layout.addWidget(provenance_heading)
        right_layout.addWidget(provenance_note)
        right_layout.addWidget(QLabel("Related Readiness Decision"))
        right_layout.addWidget(self.decision_combo)
        right_layout.addWidget(evidence_label)
        right_layout.addWidget(self.evidence_list)
        right_layout.addWidget(assessment_label)
        right_layout.addWidget(self.assessment_list)
        right_layout.addWidget(note)
        right_layout.addWidget(self.record_button)

        main_layout.addWidget(left_frame, 4)
        main_layout.addWidget(right_frame, 6)

    def set_project(self, project):
        self.project = project
        self.refresh()

    def refresh(self):
        self.findings_list.clear()
        self._populate_provenance()
        self._prepare_new_finding()

        if self.project is None:
            return

        for finding in getattr(
            self.project,
            "findings",
            [],
        ):
            item = QListWidgetItem(
                self._finding_display_text(finding)
            )
            item.setData(
                Qt.ItemDataRole.UserRole,
                finding.finding_id,
            )
            self.findings_list.addItem(item)

    @staticmethod
    def _finding_display_text(finding):
        title = finding.title or "Untitled finding"
        finding_type = getattr(
            finding.finding_type,
            "value",
            str(finding.finding_type),
        )
        return f"{finding_type} | {title}"

    def _populate_provenance(self):
        self.decision_combo.clear()
        self.decision_combo.addItem(
            "No related readiness decision",
            "",
        )
        self.evidence_list.clear()
        self.assessment_list.clear()

        if self.project is None:
            return

        decisions = getattr(
            self.project,
            "readiness_decisions",
            [],
        )
        for decision in decisions:
            outcome = getattr(
                getattr(decision, "outcome", None),
                "value",
                "No outcome",
            )
            recorded_at = getattr(
                decision,
                "recorded_at",
                "",
            )
            decision_id = getattr(
                decision,
                "decision_id",
                "",
            )
            self.decision_combo.addItem(
                f"{outcome} | {recorded_at or 'No timestamp'}",
                decision_id,
            )

        for evidence in getattr(
            self.project,
            "evidence_records",
            [],
        ):
            title = getattr(
                evidence,
                "title",
                "",
            ) or "Untitled evidence"
            evidence_id = getattr(
                evidence,
                "evidence_id",
                "",
            )

            item = QListWidgetItem(title)
            item.setData(
                Qt.ItemDataRole.UserRole,
                evidence_id,
            )
            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
            )
            item.setCheckState(
                Qt.CheckState.Unchecked
            )
            self.evidence_list.addItem(item)

        for assessment in getattr(
            self.project,
            "assessment_records",
            [],
        ):
            outcome = getattr(
                getattr(assessment, "outcome", None),
                "value",
                "No outcome",
            )
            assessor = getattr(
                assessment,
                "assessor",
                "",
            ) or "Unknown assessor"
            assessment_id = getattr(
                assessment,
                "assessment_id",
                "",
            )

            item = QListWidgetItem(
                f"{outcome} | {assessor}"
            )
            item.setData(
                Qt.ItemDataRole.UserRole,
                assessment_id,
            )
            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
            )
            item.setCheckState(
                Qt.CheckState.Unchecked
            )
            self.assessment_list.addItem(item)

    def _find_finding(self, finding_id):
        if self.project is None or not finding_id:
            return None

        for finding in getattr(
            self.project,
            "findings",
            [],
        ):
            if finding.finding_id == finding_id:
                return finding

        return None

    def _show_selected_finding(self, row):
        if row < 0:
            return

        item = self.findings_list.item(row)
        if item is None:
            return

        finding = self._find_finding(
            item.data(Qt.ItemDataRole.UserRole)
        )
        if finding is None:
            return

        self._selected_finding = finding

        self.status_label.setText(
            "Finding Status: FINDING RECORDED"
        )
        self.title_input.setText(finding.title)

        type_index = self.type_input.findData(
            finding.finding_type
        )
        if type_index >= 0:
            self.type_input.setCurrentIndex(type_index)

        self.description_input.setPlainText(
            finding.description
        )
        self.recorded_by_input.setText(
            finding.recorded_by
        )

        decision_index = self.decision_combo.findData(
            finding.related_decision_id
        )
        self.decision_combo.setCurrentIndex(
            decision_index if decision_index >= 0 else 0
        )

        self._set_checked_ids(
            self.evidence_list,
            finding.related_evidence_ids,
        )
        self._set_checked_ids(
            self.assessment_list,
            finding.related_assessment_ids,
        )

        self._set_form_read_only(True)
        self.record_button.setText("FINDING RECORDED")
        self.record_button.setEnabled(False)

    def _prepare_new_finding(self):
        self._selected_finding = None

        self.findings_list.blockSignals(True)
        self.findings_list.clearSelection()
        self.findings_list.setCurrentRow(-1)
        self.findings_list.blockSignals(False)

        self.status_label.setText(
            "Finding Status: NEW FINDING"
        )
        self.title_input.clear()
        self.type_input.setCurrentIndex(
            self.type_input.findData(
                FindingType.OBSERVATION
            )
        )
        self.description_input.clear()
        self.recorded_by_input.clear()
        self.decision_combo.setCurrentIndex(0)

        self._set_checked_ids(
            self.evidence_list,
            [],
        )
        self._set_checked_ids(
            self.assessment_list,
            [],
        )

        self._set_form_read_only(False)
        self.record_button.setText("RECORD FINDING")
        self._update_record_button()

    def _set_form_read_only(self, read_only):
        self.title_input.setReadOnly(read_only)
        self.type_input.setEnabled(not read_only)
        self.description_input.setReadOnly(read_only)
        self.recorded_by_input.setReadOnly(read_only)
        self.decision_combo.setEnabled(not read_only)
        self._set_checkable_enabled(
            self.evidence_list,
            not read_only,
        )
        self._set_checkable_enabled(
            self.assessment_list,
            not read_only,
        )

    @staticmethod
    def _set_checkable_enabled(list_widget, enabled):
        for row in range(list_widget.count()):
            item = list_widget.item(row)
            flags = item.flags()

            if enabled:
                item.setFlags(
                    flags | Qt.ItemFlag.ItemIsEnabled
                )
            else:
                item.setFlags(
                    flags & ~Qt.ItemFlag.ItemIsEnabled
                )

    @staticmethod
    def _set_checked_ids(list_widget, wanted_ids):
        wanted = set(wanted_ids or [])

        for row in range(list_widget.count()):
            item = list_widget.item(row)
            item_id = item.data(
                Qt.ItemDataRole.UserRole
            )
            item.setCheckState(
                Qt.CheckState.Checked
                if item_id in wanted
                else Qt.CheckState.Unchecked
            )

    @staticmethod
    def _checked_ids(list_widget):
        values = []

        for row in range(list_widget.count()):
            item = list_widget.item(row)
            if (
                item.checkState()
                == Qt.CheckState.Checked
            ):
                item_id = item.data(
                    Qt.ItemDataRole.UserRole
                )
                if item_id:
                    values.append(item_id)

        return values

    def _update_record_button(self, *_):
        if self._selected_finding is not None:
            self.record_button.setEnabled(False)
            return

        enabled = bool(
            self.title_input.text().strip()
            and self.description_input
            .toPlainText()
            .strip()
            and self.recorded_by_input
            .text()
            .strip()
        )

        self.record_button.setEnabled(enabled)

    def _record_finding(self):
        if self.project is None:
            return

        if self._selected_finding is not None:
            return

        title = self.title_input.text().strip()
        description = (
            self.description_input
            .toPlainText()
            .strip()
        )
        recorded_by = (
            self.recorded_by_input
            .text()
            .strip()
        )

        if not title or not description or not recorded_by:
            return

        finding = Finding(
            title=title,
            finding_type=self.type_input.currentData(),
            description=description,
            related_decision_id=(
                self.decision_combo.currentData() or ""
            ),
            related_assessment_ids=self._checked_ids(
                self.assessment_list
            ),
            related_evidence_ids=self._checked_ids(
                self.evidence_list
            ),
            recorded_by=recorded_by,
        )
        finding.mark_recorded_now()

        self.finding_recorded.emit(finding)

        # The host normally adds the emitted finding to Project.
        # Refresh only if it is already present there.
        if any(
            existing.finding_id == finding.finding_id
            for existing in getattr(
                self.project,
                "findings",
                [],
            )
        ):
            self.refresh()
            for row in range(self.findings_list.count()):
                item = self.findings_list.item(row)
                if (
                    item.data(Qt.ItemDataRole.UserRole)
                    == finding.finding_id
                ):
                    self.findings_list.setCurrentRow(row)
                    break
        else:
            self.status_label.setText(
                "Finding Status: RECORDED - awaiting project refresh"
            )
            self._set_form_read_only(True)
            self.record_button.setText("FINDING RECORDED")
            self.record_button.setEnabled(False)
