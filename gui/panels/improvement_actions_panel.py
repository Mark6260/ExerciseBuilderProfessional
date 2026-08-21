from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QScrollArea,
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

from core.improvement.action import (
    ActionPriority,
    ActionStatus,
    ImprovementAction,
)
from core.improvement.recommendation import (
    RecommendationDisposition,
)
from core.improvement.verification import (
    ImprovementVerification,
    VerificationOutcome,
)


class ActionCompletionDialog(QDialog):
    """
    Dedicated completion workflow for an in-progress improvement action.

    Completion records what was done. It does not determine whether the
    underlying finding or readiness issue has been resolved.
    """

    def __init__(self, project, action, parent=None):
        super().__init__(parent)

        self.project = project
        self.action = action

        self.setWindowTitle("Complete Improvement Action")
        self.resize(720, 620)

        self._build_ui()
        self._populate_evidence()
        self._update_record_button()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        heading = QLabel("COMPLETE IMPROVEMENT ACTION")
        heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        layout.addWidget(heading)

        action_label = QLabel(
            f"Action: {self.action.title or 'Untitled action'}"
        )
        action_label.setWordWrap(True)
        action_label.setStyleSheet(
            "font-weight: bold;"
        )
        layout.addWidget(action_label)

        warning = QLabel(
            "Recording completion confirms that the authorised task was "
            "completed. It does not demonstrate that the underlying "
            "readiness issue has been resolved."
        )
        warning.setWordWrap(True)
        warning.setStyleSheet(
            "font-style: italic;"
        )
        layout.addWidget(warning)

        layout.addWidget(QLabel("Completion Notes"))

        self.completion_notes_input = QTextEdit()
        self.completion_notes_input.setPlaceholderText(
            "Record what was completed and the outcome of the action."
        )
        self.completion_notes_input.setMinimumHeight(140)
        layout.addWidget(self.completion_notes_input)

        layout.addWidget(QLabel("Completed By"))

        self.completed_by_input = QLineEdit()
        self.completed_by_input.setPlaceholderText(
            "Completed by - name / role"
        )
        layout.addWidget(self.completed_by_input)

        evidence_heading = QLabel(
            "COMPLETION EVIDENCE"
        )
        evidence_heading.setStyleSheet(
            "font-weight: bold;"
        )
        layout.addWidget(evidence_heading)

        evidence_note = QLabel(
            "Optional: select existing evidence that supports completion "
            "of the action. This remains completion evidence only; it is "
            "not proof that the original readiness issue is resolved."
        )
        evidence_note.setWordWrap(True)
        layout.addWidget(evidence_note)

        self.evidence_list = QListWidget()
        self.evidence_list.setSelectionMode(
            QListWidget.SelectionMode.NoSelection
        )
        self.evidence_list.setMinimumHeight(180)
        layout.addWidget(self.evidence_list)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel
        )

        self.record_button = QPushButton(
            "RECORD ACTION COMPLETION"
        )
        self.record_button.setEnabled(False)
        self.button_box.addButton(
            self.record_button,
            QDialogButtonBox.ButtonRole.AcceptRole,
        )

        layout.addWidget(self.button_box)

        self.completion_notes_input.textChanged.connect(
            self._update_record_button
        )
        self.completed_by_input.textChanged.connect(
            self._update_record_button
        )
        self.record_button.clicked.connect(
            self.accept
        )
        self.button_box.rejected.connect(
            self.reject
        )

    def _populate_evidence(self):
        self.evidence_list.clear()

        if self.project is None:
            return

        for evidence in getattr(
            self.project,
            "evidence_records",
            [],
        ):
            evidence_id = getattr(
                evidence,
                "evidence_id",
                "",
            )
            if not evidence_id:
                continue

            title = (
                getattr(evidence, "title", "")
                or getattr(evidence, "description", "")
                or evidence_id
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

    def _update_record_button(self, *_):
        enabled = bool(
            self.completion_notes_input
            .toPlainText()
            .strip()
            and self.completed_by_input
            .text()
            .strip()
        )

        self.record_button.setEnabled(enabled)

    def completion_notes(self):
        return (
            self.completion_notes_input
            .toPlainText()
            .strip()
        )

    def completed_by(self):
        return (
            self.completed_by_input
            .text()
            .strip()
        )

    def evidence_ids(self):
        values = []

        for row in range(
            self.evidence_list.count()
        ):
            item = self.evidence_list.item(row)

            if (
                item.checkState()
                == Qt.CheckState.Checked
            ):
                evidence_id = item.data(
                    Qt.ItemDataRole.UserRole
                )
                if evidence_id:
                    values.append(evidence_id)

        return values


class ImprovementVerificationDialog(QDialog):
    """
    Records a professional verification assessment for a completed
    improvement action.

    Verification is separate from completion and does not alter the
    original finding, recommendation or improvement action.
    """

    def __init__(self, project, action, parent=None):
        super().__init__(parent)

        self.project = project
        self.action = action

        self.setWindowTitle("Verify Improvement")
        self.resize(760, 720)

        self._build_ui()
        self._populate_findings()
        self._populate_evidence()
        self._update_record_button()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        heading = QLabel("VERIFY IMPROVEMENT")
        heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        layout.addWidget(heading)

        action_label = QLabel(
            f"Completed action: "
            f"{self.action.title or 'Untitled action'}"
        )
        action_label.setWordWrap(True)
        action_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(action_label)

        warning = QLabel(
            "Verification is a separate professional assessment of whether "
            "the underlying issue has been resolved. Recording a verification "
            "does not rewrite the original finding, recommendation or action."
        )
        warning.setWordWrap(True)
        warning.setStyleSheet("font-style: italic;")
        layout.addWidget(warning)

        findings_heading = QLabel("RELATED FINDINGS")
        findings_heading.setStyleSheet("font-weight: bold;")
        layout.addWidget(findings_heading)

        self.findings_list = QListWidget()
        self.findings_list.setSelectionMode(
            QListWidget.SelectionMode.NoSelection
        )
        self.findings_list.setMinimumHeight(90)
        layout.addWidget(self.findings_list)

        layout.addWidget(QLabel("Verification Outcome"))

        self.outcome_input = QComboBox()
        self.outcome_input.addItem(
            "Select verification outcome...",
            None,
        )
        for outcome in VerificationOutcome:
            self.outcome_input.addItem(
                outcome.value,
                outcome,
            )
        layout.addWidget(self.outcome_input)

        layout.addWidget(QLabel("Assessment Rationale"))

        self.rationale_input = QTextEdit()
        self.rationale_input.setPlaceholderText(
            "Record the evidence-based rationale for this verification "
            "assessment."
        )
        self.rationale_input.setMinimumHeight(120)
        layout.addWidget(self.rationale_input)

        layout.addWidget(QLabel("Assessed By"))

        self.assessed_by_input = QLineEdit()
        self.assessed_by_input.setPlaceholderText(
            "Assessed by - name / role"
        )
        layout.addWidget(self.assessed_by_input)

        layout.addWidget(QLabel("Assessment Authority"))

        self.assessment_authority_input = QLineEdit()
        self.assessment_authority_input.setPlaceholderText(
            "Authority under which this assessment is made"
        )
        layout.addWidget(self.assessment_authority_input)

        evidence_heading = QLabel("VERIFICATION EVIDENCE")
        evidence_heading.setStyleSheet("font-weight: bold;")
        layout.addWidget(evidence_heading)

        evidence_note = QLabel(
            "Optional: select existing evidence considered during the "
            "verification assessment."
        )
        evidence_note.setWordWrap(True)
        layout.addWidget(evidence_note)

        self.evidence_list = QListWidget()
        self.evidence_list.setSelectionMode(
            QListWidget.SelectionMode.NoSelection
        )
        self.evidence_list.setMinimumHeight(140)
        layout.addWidget(self.evidence_list)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel
        )

        self.record_button = QPushButton(
            "RECORD VERIFICATION"
        )
        self.record_button.setEnabled(False)
        self.button_box.addButton(
            self.record_button,
            QDialogButtonBox.ButtonRole.AcceptRole,
        )
        layout.addWidget(self.button_box)

        self.outcome_input.currentIndexChanged.connect(
            self._update_record_button
        )
        self.rationale_input.textChanged.connect(
            self._update_record_button
        )
        self.assessed_by_input.textChanged.connect(
            self._update_record_button
        )
        self.assessment_authority_input.textChanged.connect(
            self._update_record_button
        )
        self.record_button.clicked.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def _populate_findings(self):
        self.findings_list.clear()
        wanted_ids = set(
            getattr(
                self.action,
                "related_finding_ids",
                [],
            )
        )

        for finding in getattr(
            self.project,
            "findings",
            [],
        ):
            if finding.finding_id not in wanted_ids:
                continue

            finding_type = getattr(
                finding.finding_type,
                "value",
                str(finding.finding_type),
            )
            item = QListWidgetItem(
                f"{finding_type} | "
                f"{finding.title or 'Untitled finding'}"
            )
            item.setData(
                Qt.ItemDataRole.UserRole,
                finding.finding_id,
            )
            item.setFlags(
                item.flags()
                & ~Qt.ItemFlag.ItemIsEnabled
            )
            self.findings_list.addItem(item)

    def _populate_evidence(self):
        self.evidence_list.clear()

        for evidence in getattr(
            self.project,
            "evidence_records",
            [],
        ):
            evidence_id = getattr(
                evidence,
                "evidence_id",
                "",
            )
            if not evidence_id:
                continue

            title = (
                getattr(evidence, "title", "")
                or getattr(evidence, "description", "")
                or evidence_id
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

    def _update_record_button(self, *_):
        enabled = bool(
            self.outcome_input.currentData() is not None
            and self.rationale_input.toPlainText().strip()
            and self.assessed_by_input.text().strip()
            and self.assessment_authority_input.text().strip()
        )
        self.record_button.setEnabled(enabled)

    def outcome(self):
        return self.outcome_input.currentData()

    def rationale(self):
        return self.rationale_input.toPlainText().strip()

    def assessed_by(self):
        return self.assessed_by_input.text().strip()

    def assessment_authority(self):
        return self.assessment_authority_input.text().strip()

    def evidence_ids(self):
        values = []

        for row in range(self.evidence_list.count()):
            item = self.evidence_list.item(row)
            if item.checkState() == Qt.CheckState.Checked:
                evidence_id = item.data(
                    Qt.ItemDataRole.UserRole
                )
                if evidence_id:
                    values.append(evidence_id)

        return values


class VerificationRecordDialog(QDialog):
    """
    Read-only presentation of an immutable improvement verification record.
    """

    def __init__(self, project, verification, parent=None):
        super().__init__(parent)

        self.project = project
        self.verification = verification

        self.setWindowTitle("Improvement Verification Record")
        self.resize(760, 620)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        heading = QLabel("IMPROVEMENT VERIFICATION RECORD")
        heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        layout.addWidget(heading)

        outcome = getattr(
            self.verification.outcome,
            "value",
            str(self.verification.outcome),
        )
        follow_up = self.verification.follow_up_state().value

        outcome_label = QLabel(
            f"Outcome: {outcome}"
        )
        outcome_label.setStyleSheet(
            "font-weight: bold;"
        )
        layout.addWidget(outcome_label)

        follow_up_label = QLabel(
            f"Follow-up state: {follow_up}"
        )
        follow_up_label.setStyleSheet(
            "font-weight: bold;"
        )
        layout.addWidget(follow_up_label)

        layout.addWidget(QLabel("Assessment Rationale"))

        rationale = QTextEdit()
        rationale.setPlainText(
            self.verification.rationale or "-"
        )
        rationale.setReadOnly(True)
        rationale.setMinimumHeight(140)
        layout.addWidget(rationale)

        layout.addWidget(QLabel(
            f"Assessed by: "
            f"{self.verification.assessed_by or '-'}"
        ))
        layout.addWidget(QLabel(
            "Assessment authority: "
            f"{self.verification.assessment_authority or '-'}"
        ))
        layout.addWidget(QLabel(
            f"Recorded: "
            f"{self.verification.recorded_at or '-'}"
        ))

        evidence_heading = QLabel("VERIFICATION EVIDENCE")
        evidence_heading.setStyleSheet(
            "font-weight: bold;"
        )
        layout.addWidget(evidence_heading)

        evidence_list = QListWidget()
        evidence_list.setSelectionMode(
            QListWidget.SelectionMode.NoSelection
        )
        evidence_list.setMinimumHeight(150)

        evidence_ids = list(
            getattr(
                self.verification,
                "related_evidence_ids",
                [],
            )
        )

        if evidence_ids:
            for evidence_id in evidence_ids:
                title = self._find_evidence_title(
                    evidence_id
                )
                item = QListWidgetItem(title)
                item.setFlags(
                    item.flags()
                    & ~Qt.ItemFlag.ItemIsEnabled
                )
                evidence_list.addItem(item)
        else:
            item = QListWidgetItem(
                "No verification evidence linked."
            )
            item.setFlags(
                item.flags()
                & ~Qt.ItemFlag.ItemIsEnabled
            )
            evidence_list.addItem(item)

        layout.addWidget(evidence_list)

        note = QLabel(
            "This record is read-only. Verification does not rewrite the "
            "original finding, recommendation or improvement action."
        )
        note.setWordWrap(True)
        note.setStyleSheet(
            "font-style: italic;"
        )
        layout.addWidget(note)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close
        )
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _find_evidence_title(self, evidence_id):
        for evidence in getattr(
            self.project,
            "evidence_records",
            [],
        ):
            if (
                getattr(evidence, "evidence_id", "")
                == evidence_id
            ):
                return (
                    getattr(evidence, "title", "")
                    or getattr(evidence, "description", "")
                    or evidence_id
                )

        return evidence_id


class ImprovementLineageDialog(QDialog):
    """
    Read-only view of the provable improvement lineage for an action.

    The lineage is assembled from existing record identifiers only.
    Missing links are displayed honestly rather than inferred.
    """

    def __init__(self, project, action, parent=None):
        super().__init__(parent)

        self.project = project
        self.action = action

        self.setWindowTitle("Improvement Lineage")
        self.resize(820, 720)

        self._build_ui()

    def _build_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(18, 18, 18, 18)
        outer_layout.setSpacing(12)

        heading = QLabel("IMPROVEMENT LINEAGE")
        heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        outer_layout.addWidget(heading)

        note = QLabel(
            "This read-only view shows the improvement chain that "
            "Exercise Director can prove from recorded identifiers. "
            "It does not alter or infer missing records."
        )
        note.setWordWrap(True)
        note.setStyleSheet("font-style: italic;")
        outer_layout.addWidget(note)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        chain = self._resolve_lineage()

        for index, node in enumerate(chain):
            frame = QFrame()
            frame.setFrameShape(QFrame.Shape.StyledPanel)
            frame_layout = QVBoxLayout(frame)
            frame_layout.setContentsMargins(12, 10, 12, 10)
            frame_layout.setSpacing(4)

            type_label = QLabel(node["type"])
            type_label.setStyleSheet(
                "font-weight: bold;"
            )
            frame_layout.addWidget(type_label)

            title_label = QLabel(node["title"])
            title_label.setWordWrap(True)
            if node.get("current"):
                title_label.setStyleSheet(
                    "font-weight: bold; text-decoration: underline;"
                )
            frame_layout.addWidget(title_label)

            for detail in node.get("details", []):
                detail_label = QLabel(detail)
                detail_label.setWordWrap(True)
                frame_layout.addWidget(detail_label)

            if node.get("current"):
                current_label = QLabel("CURRENTLY SELECTED ACTION")
                current_label.setStyleSheet(
                    "font-weight: bold;"
                )
                frame_layout.addWidget(current_label)

            layout.addWidget(frame)

            if index < len(chain) - 1:
                arrow = QLabel("↓")
                arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
                arrow.setStyleSheet(
                    "font-size: 18px; font-weight: bold;"
                )
                layout.addWidget(arrow)

        layout.addStretch()

        scroll.setWidget(content)
        outer_layout.addWidget(scroll)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close
        )
        button_box.rejected.connect(self.reject)
        outer_layout.addWidget(button_box)

    def _resolve_lineage(self):
        actions = list(
            getattr(
                self.project,
                "improvement_actions",
                [],
            )
        )
        verifications = list(
            getattr(
                self.project,
                "improvement_verifications",
                [],
            )
        )
        recommendations = list(
            getattr(
                self.project,
                "recommendations",
                [],
            )
        )
        findings = list(
            getattr(
                self.project,
                "findings",
                [],
            )
        )

        action_by_id = {
            item.action_id: item
            for item in actions
        }
        verification_by_id = {
            item.verification_id: item
            for item in verifications
        }
        recommendation_by_id = {
            item.recommendation_id: item
            for item in recommendations
        }
        finding_by_id = {
            item.finding_id: item
            for item in findings
        }

        current = self.action

        # Walk backwards through verification provenance to the earliest
        # action that can be proved.
        action_chain = [current]
        visited_action_ids = {current.action_id}

        while True:
            verification_ids = list(
                getattr(
                    action_chain[0],
                    "related_verification_ids",
                    [],
                )
            )
            if not verification_ids:
                break

            verification = verification_by_id.get(
                verification_ids[0]
            )
            if verification is None:
                break

            parent_action = action_by_id.get(
                verification.related_action_id
            )
            if (
                parent_action is None
                or parent_action.action_id in visited_action_ids
            ):
                break

            action_chain.insert(0, parent_action)
            visited_action_ids.add(parent_action.action_id)

        nodes = []

        root_action = action_chain[0]

        for finding_id in getattr(
            root_action,
            "related_finding_ids",
            [],
        ):
            finding = finding_by_id.get(finding_id)
            if finding is None:
                nodes.append({
                    "type": "FINDING",
                    "title": f"Missing recorded finding: {finding_id}",
                    "details": [],
                })
                continue

            finding_type = getattr(
                getattr(finding, "finding_type", ""),
                "value",
                str(getattr(finding, "finding_type", "")),
            )
            nodes.append({
                "type": "FINDING",
                "title": finding.title or "Untitled finding",
                "details": (
                    [f"Type: {finding_type}"]
                    if finding_type
                    else []
                ),
            })

        for recommendation_id in getattr(
            root_action,
            "related_recommendation_ids",
            [],
        ):
            recommendation = recommendation_by_id.get(
                recommendation_id
            )
            if recommendation is None:
                nodes.append({
                    "type": "RECOMMENDATION",
                    "title": (
                        "Missing recorded recommendation: "
                        f"{recommendation_id}"
                    ),
                    "details": [],
                })
                continue

            disposition = getattr(
                getattr(recommendation, "disposition", ""),
                "value",
                str(getattr(recommendation, "disposition", "")),
            )
            nodes.append({
                "type": "RECOMMENDATION",
                "title": (
                    recommendation.title
                    or "Untitled recommendation"
                ),
                "details": (
                    [f"Disposition: {disposition}"]
                    if disposition
                    else []
                ),
            })

        for index, action in enumerate(action_chain):
            status = getattr(
                getattr(action, "status", ""),
                "value",
                str(getattr(action, "status", "")),
            )
            nodes.append({
                "type": (
                    "IMPROVEMENT ACTION"
                    if index == 0
                    else "FOLLOW-UP IMPROVEMENT ACTION"
                ),
                "title": action.title or "Untitled action",
                "details": [
                    f"Status: {status or '-'}",
                    f"Owner: {getattr(action, 'owner', '') or '-'}",
                ],
                "current": action.action_id == current.action_id,
            })

            verification = next(
                (
                    item
                    for item in verifications
                    if item.related_action_id == action.action_id
                ),
                None,
            )

            if verification is not None:
                outcome = getattr(
                    verification.outcome,
                    "value",
                    str(verification.outcome),
                )
                nodes.append({
                    "type": "VERIFICATION",
                    "title": f"Outcome: {outcome}",
                    "details": [
                        "Follow-up state: "
                        f"{verification.follow_up_state().value}",
                        "Assessed by: "
                        f"{verification.assessed_by or '-'}",
                        "Recorded: "
                        f"{verification.recorded_at or '-'}",
                    ],
                })

        # Show direct follow-up actions from the final action if they exist
        # and are not already in the backwards-resolved chain.
        final_action = action_chain[-1]
        final_verification = next(
            (
                item
                for item in verifications
                if item.related_action_id == final_action.action_id
            ),
            None,
        )

        if final_verification is not None:
            existing_ids = {
                item.action_id
                for item in action_chain
            }
            for candidate in actions:
                if candidate.action_id in existing_ids:
                    continue
                if final_verification.verification_id not in getattr(
                    candidate,
                    "related_verification_ids",
                    [],
                ):
                    continue

                status = getattr(
                    getattr(candidate, "status", ""),
                    "value",
                    str(getattr(candidate, "status", "")),
                )
                nodes.append({
                    "type": "FOLLOW-UP IMPROVEMENT ACTION",
                    "title": (
                        candidate.title
                        or "Untitled action"
                    ),
                    "details": [
                        f"Status: {status or '-'}",
                        f"Owner: {candidate.owner or '-'}",
                    ],
                    "current": (
                        candidate.action_id == current.action_id
                    ),
                })

        if not nodes:
            nodes.append({
                "type": "IMPROVEMENT ACTION",
                "title": current.title or "Untitled action",
                "details": ["No additional lineage is recorded."],
                "current": True,
            })

        return nodes


class ImprovementActionsPanel(QWidget):
    """
    Records authorised improvement actions arising from accepted
    recommendations.

    An accepted recommendation does not automatically become an action.
    The user must deliberately create and authorise the action.
    """

    action_recorded = Signal(object)
    action_status_changed = Signal(object)
    verification_recorded = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.project = None
        self._selected_action = None
        self._pending_follow_up_verification_id = ""

        self._build_ui()

        self.actions_list.currentRowChanged.connect(
            self._show_selected_action
        )
        self.new_button.clicked.connect(
            self._prepare_new_action
        )

        self.title_input.textChanged.connect(
            self._update_record_button
        )
        self.description_input.textChanged.connect(
            self._update_record_button
        )
        self.owner_input.textChanged.connect(
            self._update_record_button
        )
        self.authorised_by_input.textChanged.connect(
            self._update_record_button
        )
        self.recommendations_list.itemChanged.connect(
            self._recommendation_selection_changed
        )

        self.record_button.clicked.connect(
            self._record_action
        )
        self.change_status_button.clicked.connect(
            self._start_status_change
        )
        self.next_status_input.currentIndexChanged.connect(
            self._update_status_change_button
        )
        self.status_rationale_input.textChanged.connect(
            self._update_status_change_button
        )
        self.status_changed_by_input.textChanged.connect(
            self._update_status_change_button
        )
        self.record_status_change_button.clicked.connect(
            self._record_status_change
        )
        self.complete_action_button.clicked.connect(
            self._open_completion_dialog
        )
        self.verify_improvement_button.clicked.connect(
            self._open_verification_dialog
        )
        self.view_verification_button.clicked.connect(
            self._open_verification_record_dialog
        )
        self.follow_up_action_button.clicked.connect(
            self._prepare_follow_up_action
        )
        self.view_lineage_button.clicked.connect(
            self._open_lineage_dialog
        )
        self.action_filter_input.currentIndexChanged.connect(
            self._apply_action_filter
        )

    def _build_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # -------------------------------------------------
        # Recorded actions
        # -------------------------------------------------

        left_frame = QFrame()
        left_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )
        left_layout = QVBoxLayout(left_frame)

        left_heading = QLabel(
            "RECORDED IMPROVEMENT ACTIONS"
        )
        left_heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        left_note = QLabel(
            "Improvement actions are authorised tasks arising from "
            "exercise learning. Select a recorded action to inspect "
            "its immutable authorisation record."
        )
        left_note.setWordWrap(True)

        self.overview_frame = QFrame()
        self.overview_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )
        overview_layout = QVBoxLayout(
            self.overview_frame
        )
        overview_layout.setContentsMargins(
            10, 8, 10, 8
        )
        overview_layout.setSpacing(3)

        overview_heading = QLabel(
            "IMPROVEMENT OVERVIEW"
        )
        overview_heading.setStyleSheet(
            "font-weight: bold;"
        )

        self.overview_actions_label = QLabel("")
        self.overview_actions_label.setWordWrap(True)

        self.overview_verification_label = QLabel("")
        self.overview_verification_label.setWordWrap(True)

        self.overview_follow_up_label = QLabel("")
        self.overview_follow_up_label.setWordWrap(True)

        overview_layout.addWidget(overview_heading)
        overview_layout.addWidget(
            self.overview_actions_label
        )
        overview_layout.addWidget(
            self.overview_verification_label
        )
        overview_layout.addWidget(
            self.overview_follow_up_label
        )

        self.action_filter_input = QComboBox()
        self.action_filter_input.addItem("All", "all")
        self.action_filter_input.addItem("Open", "open")
        self.action_filter_input.addItem(
            "Completed",
            "completed",
        )
        self.action_filter_input.addItem(
            "Further Improvement",
            "further_improvement",
        )
        self.action_filter_input.addItem(
            "Critical",
            "critical",
        )

        self.actions_list = QListWidget()

        self.new_button = QPushButton(
            "NEW IMPROVEMENT ACTION"
        )

        left_layout.addWidget(left_heading)
        left_layout.addWidget(left_note)
        left_layout.addWidget(self.overview_frame)
        left_layout.addWidget(self.action_filter_input)
        left_layout.addWidget(self.actions_list)
        left_layout.addWidget(self.new_button)

        # -------------------------------------------------
        # Action creation / inspection
        # -------------------------------------------------

        right_frame = QFrame()
        right_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        right_outer_layout = QVBoxLayout(right_frame)
        right_outer_layout.setContentsMargins(0, 0, 0, 0)

        self.review_scroll_area = QScrollArea()
        self.review_scroll_area.setWidgetResizable(True)
        self.review_scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        review_content = QWidget()
        right_layout = QVBoxLayout(review_content)
        right_layout.setContentsMargins(12, 12, 12, 12)
        right_layout.setSpacing(8)

        self.review_scroll_area.setWidget(review_content)
        right_outer_layout.addWidget(self.review_scroll_area)

        heading = QLabel(
            "IMPROVEMENT ACTION REVIEW"
        )
        heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.status_label = QLabel(
            "Action Status: NEW ACTION"
        )
        self.status_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText(
            "Improvement action title"
        )

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText(
            "Describe the authorised action to be completed."
        )
        self.description_input.setMinimumHeight(100)

        provenance_heading = QLabel(
            "AUTHORISED BASIS"
        )
        provenance_heading.setStyleSheet(
            "font-weight: bold;"
        )

        provenance_note = QLabel(
            "Select an Accepted or Accepted In Part recommendation. "
            "Exercise Director will preserve the recommendation and "
            "its related finding provenance."
        )
        provenance_note.setWordWrap(True)

        self.recommendations_list = QListWidget()
        self.recommendations_list.setSelectionMode(
            QListWidget.SelectionMode.NoSelection
        )
        self.recommendations_list.setMinimumHeight(100)

        self.findings_heading = QLabel(
            "RELATED FINDINGS"
        )
        self.findings_heading.setStyleSheet(
            "font-weight: bold;"
        )

        self.findings_list = QListWidget()
        self.findings_list.setSelectionMode(
            QListWidget.SelectionMode.NoSelection
        )
        self.findings_list.setMinimumHeight(80)

        ownership_heading = QLabel(
            "ACTION OWNERSHIP"
        )
        ownership_heading.setStyleSheet(
            "font-weight: bold;"
        )

        self.owner_input = QLineEdit()
        self.owner_input.setPlaceholderText(
            "Action owner - person / team / role"
        )

        self.priority_input = QComboBox()
        for priority in ActionPriority:
            self.priority_input.addItem(
                priority.value,
                priority,
            )

        self.target_date_input = QDateEdit()
        self.target_date_input.setCalendarPopup(True)
        self.target_date_input.setDisplayFormat(
            "yyyy-MM-dd"
        )
        self.target_date_input.setDate(
            QDate.currentDate().addDays(30)
        )

        authorisation_heading = QLabel(
            "AUTHORISATION"
        )
        authorisation_heading.setStyleSheet(
            "font-weight: bold;"
        )

        authorisation_note = QLabel(
            "Recording this action confirms that the task has been "
            "deliberately authorised. It does not demonstrate that the "
            "underlying readiness issue has been resolved."
        )
        authorisation_note.setWordWrap(True)
        authorisation_note.setStyleSheet(
            "font-style: italic;"
        )

        self.authorised_by_input = QLineEdit()
        self.authorised_by_input.setPlaceholderText(
            "Authorised by - name / role"
        )

        self.authorised_at_label = QLabel(
            "Authorised at: Recorded when action is authorised"
        )

        lifecycle_heading = QLabel(
            "ACTION LIFECYCLE"
        )
        lifecycle_heading.setStyleSheet(
            "font-weight: bold;"
        )

        self.lifecycle_label = QLabel(
            ActionStatus.NOT_STARTED.value
        )
        self.lifecycle_label.setStyleSheet(
            "font-weight: bold;"
        )

        lifecycle_note = QLabel(
            "Lifecycle status is changed deliberately and separately from "
            "action authorisation. GREEN 7-6A records status progression "
            "and rationale. Completion evidence remains a later controlled "
            "step."
        )
        lifecycle_note.setWordWrap(True)
        lifecycle_note.setStyleSheet(
            "font-style: italic;"
        )

        self.lifecycle_record_detail = QLabel("")
        self.lifecycle_record_detail.setWordWrap(True)
        self.lifecycle_record_detail.setVisible(False)

        self.change_status_button = QPushButton(
            "CHANGE ACTION STATUS"
        )
        self.change_status_button.setVisible(False)

        self.next_status_input = QComboBox()
        self.next_status_input.setVisible(False)

        self.status_rationale_input = QTextEdit()
        self.status_rationale_input.setPlaceholderText(
            "Record the reason for this lifecycle status change."
        )
        self.status_rationale_input.setMinimumHeight(80)
        self.status_rationale_input.setVisible(False)

        self.status_changed_by_input = QLineEdit()
        self.status_changed_by_input.setPlaceholderText(
            "Status changed by - name / role"
        )
        self.status_changed_by_input.setVisible(False)

        self.record_status_change_button = QPushButton(
            "RECORD STATUS CHANGE"
        )
        self.record_status_change_button.setEnabled(False)
        self.record_status_change_button.setVisible(False)

        self.complete_action_button = QPushButton(
            "COMPLETE ACTION"
        )
        self.complete_action_button.setVisible(False)

        self.verify_improvement_button = QPushButton(
            "VERIFY IMPROVEMENT"
        )
        self.verify_improvement_button.setVisible(False)

        self.verification_record_frame = QFrame()
        self.verification_record_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )
        verification_layout = QVBoxLayout(
            self.verification_record_frame
        )
        verification_layout.setContentsMargins(
            10, 8, 10, 8
        )
        verification_layout.setSpacing(4)

        verification_heading = QLabel(
            "IMPROVEMENT VERIFICATION"
        )
        verification_heading.setStyleSheet(
            "font-weight: bold;"
        )

        self.verification_outcome_label = QLabel("")
        self.verification_outcome_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.verification_follow_up_label = QLabel("")
        self.verification_follow_up_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.view_verification_button = QPushButton(
            "VIEW VERIFICATION RECORD"
        )

        self.follow_up_action_button = QPushButton(
            "CREATE FOLLOW-UP IMPROVEMENT ACTION"
        )
        self.follow_up_action_button.setVisible(False)

        verification_layout.addWidget(
            verification_heading
        )
        verification_layout.addWidget(
            self.verification_outcome_label
        )
        verification_layout.addWidget(
            self.verification_follow_up_label
        )
        verification_layout.addWidget(
            self.view_verification_button
        )
        verification_layout.addWidget(
            self.follow_up_action_button
        )

        self.verification_record_frame.setVisible(False)

        self.view_lineage_button = QPushButton(
            "VIEW IMPROVEMENT LINEAGE"
        )
        self.view_lineage_button.setVisible(False)

        self.record_button = QPushButton(
            "RECORD AUTHORISED ACTION"
        )
        self.record_button.setEnabled(False)

        right_layout.addWidget(heading)
        right_layout.addWidget(self.status_label)
        right_layout.addWidget(QLabel("Title"))
        right_layout.addWidget(self.title_input)
        right_layout.addWidget(QLabel("Description"))
        right_layout.addWidget(self.description_input)

        right_layout.addWidget(provenance_heading)
        right_layout.addWidget(provenance_note)
        right_layout.addWidget(self.recommendations_list)
        right_layout.addWidget(self.findings_heading)
        right_layout.addWidget(self.findings_list)

        right_layout.addWidget(ownership_heading)
        right_layout.addWidget(QLabel("Owner"))
        right_layout.addWidget(self.owner_input)
        right_layout.addWidget(QLabel("Priority"))
        right_layout.addWidget(self.priority_input)
        right_layout.addWidget(QLabel("Target Date"))
        right_layout.addWidget(self.target_date_input)

        right_layout.addWidget(authorisation_heading)
        right_layout.addWidget(authorisation_note)
        right_layout.addWidget(self.authorised_by_input)
        right_layout.addWidget(self.authorised_at_label)

        right_layout.addWidget(lifecycle_heading)
        right_layout.addWidget(self.lifecycle_label)
        right_layout.addWidget(lifecycle_note)
        right_layout.addWidget(self.lifecycle_record_detail)
        right_layout.addWidget(self.change_status_button)
        right_layout.addWidget(self.next_status_input)
        right_layout.addWidget(self.status_rationale_input)
        right_layout.addWidget(self.status_changed_by_input)
        right_layout.addWidget(self.record_status_change_button)
        right_layout.addWidget(self.complete_action_button)
        right_layout.addWidget(self.verify_improvement_button)
        right_layout.addWidget(self.verification_record_frame)
        right_layout.addWidget(self.view_lineage_button)
        right_layout.addWidget(self.record_button)

        main_layout.addWidget(left_frame, 4)
        main_layout.addWidget(right_frame, 6)

    def set_project(self, project):
        self.project = project
        self.refresh()

    def refresh(self):
        self._populate_recommendations()
        self._prepare_new_action()
        self._refresh_improvement_overview()
        self._apply_action_filter()

    def _apply_action_filter(self, *_):
        self.actions_list.blockSignals(True)
        self.actions_list.clear()

        if self.project is None:
            self.actions_list.blockSignals(False)
            return

        filter_key = self.action_filter_input.currentData()
        actions = list(
            getattr(
                self.project,
                "improvement_actions",
                [],
            )
        )

        for action in actions:
            if not self._action_matches_filter(
                action,
                filter_key,
            ):
                continue

            item = QListWidgetItem(
                self._action_display_text(action)
            )
            item.setData(
                Qt.ItemDataRole.UserRole,
                action.action_id,
            )
            self.actions_list.addItem(item)

        self.actions_list.blockSignals(False)

    def _action_matches_filter(
        self,
        action,
        filter_key,
    ):
        if filter_key in (None, "all"):
            return True

        if filter_key == "open":
            return action.status in {
                ActionStatus.NOT_STARTED,
                ActionStatus.IN_PROGRESS,
                ActionStatus.BLOCKED,
            }

        if filter_key == "completed":
            return action.status == ActionStatus.COMPLETED

        if filter_key == "critical":
            return action.priority == ActionPriority.CRITICAL

        if filter_key == "further_improvement":
            verification = self._find_verification_for_action(
                action
            )
            return bool(
                verification is not None
                and verification.follow_up_state().value
                == "Further Improvement Required"
            )

        return True

    def _refresh_improvement_overview(self):
        actions = list(
            getattr(
                self.project,
                "improvement_actions",
                [],
            )
        ) if self.project is not None else []

        verifications = list(
            getattr(
                self.project,
                "improvement_verifications",
                [],
            )
        ) if self.project is not None else []

        action_counts = {
            status: 0
            for status in ActionStatus
        }
        for action in actions:
            if action.status in action_counts:
                action_counts[action.status] += 1

        verification_counts = {
            outcome: 0
            for outcome in VerificationOutcome
        }
        follow_up_counts = {}

        for verification in verifications:
            if verification.outcome in verification_counts:
                verification_counts[verification.outcome] += 1

            follow_up_value = (
                verification.follow_up_state().value
            )
            follow_up_counts[follow_up_value] = (
                follow_up_counts.get(follow_up_value, 0) + 1
            )

        self.overview_actions_label.setText(
            "ACTIONS  |  "
            f"Total {len(actions)}  •  "
            f"Not Started "
            f"{action_counts[ActionStatus.NOT_STARTED]}  •  "
            f"In Progress "
            f"{action_counts[ActionStatus.IN_PROGRESS]}  •  "
            f"Blocked "
            f"{action_counts[ActionStatus.BLOCKED]}  •  "
            f"Completed "
            f"{action_counts[ActionStatus.COMPLETED]}  •  "
            f"Cancelled "
            f"{action_counts[ActionStatus.CANCELLED]}"
        )

        self.overview_verification_label.setText(
            "VERIFICATION  |  "
            f"Resolved "
            f"{verification_counts[VerificationOutcome.RESOLVED]}  •  "
            f"Partially Resolved "
            f"{verification_counts[VerificationOutcome.PARTIALLY_RESOLVED]}  •  "
            f"Not Resolved "
            f"{verification_counts[VerificationOutcome.NOT_RESOLVED]}  •  "
            f"Insufficient Evidence "
            f"{verification_counts[VerificationOutcome.INSUFFICIENT_EVIDENCE]}"
        )

        ordered_follow_up_states = [
            "Closed",
            "Further Improvement Required",
            "Further Evidence Required",
        ]
        extra_states = sorted(
            state
            for state in follow_up_counts
            if state not in ordered_follow_up_states
        )

        follow_up_parts = []
        for state in ordered_follow_up_states + extra_states:
            follow_up_parts.append(
                f"{state} {follow_up_counts.get(state, 0)}"
            )

        self.overview_follow_up_label.setText(
            "FOLLOW-UP  |  "
            + "  •  ".join(follow_up_parts)
        )

    @staticmethod
    def _action_display_text(action):
        title = action.title or "Untitled action"
        priority = getattr(
            action.priority,
            "value",
            str(action.priority),
        )
        status = getattr(
            action.status,
            "value",
            str(action.status),
        )
        return f"{priority} | {title} | {status}"

    def _populate_recommendations(self):
        self.recommendations_list.clear()

        if self.project is None:
            return

        allowed = {
            RecommendationDisposition.ACCEPTED,
            RecommendationDisposition.ACCEPTED_IN_PART,
        }

        for recommendation in getattr(
            self.project,
            "recommendations",
            [],
        ):
            if recommendation.disposition not in allowed:
                continue

            item = QListWidgetItem(
                f"{recommendation.disposition.value} | "
                f"{recommendation.title or 'Untitled recommendation'}"
            )
            item.setData(
                Qt.ItemDataRole.UserRole,
                recommendation.recommendation_id,
            )
            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
            )
            item.setCheckState(
                Qt.CheckState.Unchecked
            )
            self.recommendations_list.addItem(item)

    def _recommendation_selection_changed(self, changed_item):
        if (
            changed_item is not None
            and changed_item.checkState()
            == Qt.CheckState.Checked
        ):
            self.recommendations_list.blockSignals(True)

            for row in range(
                self.recommendations_list.count()
            ):
                item = self.recommendations_list.item(row)
                if item is not changed_item:
                    item.setCheckState(
                        Qt.CheckState.Unchecked
                    )

            self.recommendations_list.blockSignals(False)

        self._populate_related_findings()
        self._update_record_button()

    def _selected_recommendation_id(self):
        for row in range(
            self.recommendations_list.count()
        ):
            item = self.recommendations_list.item(row)
            if (
                item.checkState()
                == Qt.CheckState.Checked
            ):
                return item.data(
                    Qt.ItemDataRole.UserRole
                )
        return ""

    def _find_recommendation(
        self,
        recommendation_id,
    ):
        if self.project is None:
            return None

        for recommendation in getattr(
            self.project,
            "recommendations",
            [],
        ):
            if (
                recommendation.recommendation_id
                == recommendation_id
            ):
                return recommendation

        return None

    def _find_action(self, action_id):
        if self.project is None:
            return None

        for action in getattr(
            self.project,
            "improvement_actions",
            [],
        ):
            if action.action_id == action_id:
                return action

        return None

    def _populate_related_findings(self):
        self.findings_list.clear()

        recommendation = self._find_recommendation(
            self._selected_recommendation_id()
        )

        if recommendation is None:
            return

        wanted_ids = set(
            recommendation.related_finding_ids
        )

        for finding in getattr(
            self.project,
            "findings",
            [],
        ):
            if finding.finding_id not in wanted_ids:
                continue

            finding_type = getattr(
                finding.finding_type,
                "value",
                str(finding.finding_type),
            )
            item = QListWidgetItem(
                f"{finding_type} | "
                f"{finding.title or 'Untitled finding'}"
            )
            item.setData(
                Qt.ItemDataRole.UserRole,
                finding.finding_id,
            )
            item.setFlags(
                item.flags()
                & ~Qt.ItemFlag.ItemIsEnabled
            )
            item.setCheckState(
                Qt.CheckState.Checked
            )
            self.findings_list.addItem(item)

    def _prepare_new_action(self):
        self._pending_follow_up_verification_id = ""
        self._selected_action = None

        self.actions_list.blockSignals(True)
        self.actions_list.clearSelection()
        self.actions_list.setCurrentRow(-1)
        self.actions_list.blockSignals(False)

        self.status_label.setText(
            "Action Status: NEW ACTION"
        )
        self.title_input.clear()
        self.description_input.clear()
        self.owner_input.clear()

        priority_index = self.priority_input.findData(
            ActionPriority.MEDIUM
        )
        self.priority_input.setCurrentIndex(
            priority_index
            if priority_index >= 0
            else 0
        )

        self.target_date_input.setDate(
            QDate.currentDate().addDays(30)
        )
        self.authorised_by_input.clear()
        self.authorised_at_label.setText(
            "Authorised at: Recorded when action is authorised"
        )
        self.lifecycle_label.setText(
            ActionStatus.NOT_STARTED.value
        )
        self._reset_status_change_controls()

        self.recommendations_list.blockSignals(True)
        for row in range(
            self.recommendations_list.count()
        ):
            self.recommendations_list.item(row).setCheckState(
                Qt.CheckState.Unchecked
            )
        self.recommendations_list.blockSignals(False)

        self.findings_list.clear()
        self.view_lineage_button.setVisible(False)
        self._set_form_read_only(False)
        self.record_button.setText(
            "RECORD AUTHORISED ACTION"
        )
        self._update_record_button()

    def _show_selected_action(self, row):
        if row < 0:
            return

        item = self.actions_list.item(row)
        if item is None:
            return

        action = self._find_action(
            item.data(Qt.ItemDataRole.UserRole)
        )
        if action is None:
            return

        self._selected_action = action

        self.status_label.setText(
            "Action Status: ACTION AUTHORISED"
        )
        self.title_input.setText(action.title)
        self.description_input.setPlainText(
            action.description
        )
        self.owner_input.setText(action.owner)

        priority_index = self.priority_input.findData(
            action.priority
        )
        if priority_index >= 0:
            self.priority_input.setCurrentIndex(
                priority_index
            )

        target_date = QDate.fromString(
            action.target_date,
            "yyyy-MM-dd",
        )
        if target_date.isValid():
            self.target_date_input.setDate(
                target_date
            )

        self.authorised_by_input.setText(
            action.authorised_by
        )
        self.authorised_at_label.setText(
            "Authorised at: "
            f"{action.authorised_at or '-'}"
        )
        self.lifecycle_label.setText(
            action.status.value
        )
        self._show_lifecycle_state(action)

        wanted_recommendations = set(
            action.related_recommendation_ids
        )

        self.recommendations_list.blockSignals(True)
        for rec_row in range(
            self.recommendations_list.count()
        ):
            rec_item = self.recommendations_list.item(
                rec_row
            )
            rec_id = rec_item.data(
                Qt.ItemDataRole.UserRole
            )
            rec_item.setCheckState(
                Qt.CheckState.Checked
                if rec_id in wanted_recommendations
                else Qt.CheckState.Unchecked
            )
        self.recommendations_list.blockSignals(False)

        self.findings_list.clear()
        wanted_findings = set(
            action.related_finding_ids
        )

        for finding in getattr(
            self.project,
            "findings",
            [],
        ):
            if finding.finding_id not in wanted_findings:
                continue

            finding_type = getattr(
                finding.finding_type,
                "value",
                str(finding.finding_type),
            )
            finding_item = QListWidgetItem(
                f"{finding_type} | "
                f"{finding.title or 'Untitled finding'}"
            )
            finding_item.setData(
                Qt.ItemDataRole.UserRole,
                finding.finding_id,
            )
            finding_item.setCheckState(
                Qt.CheckState.Checked
            )
            self.findings_list.addItem(
                finding_item
            )

        self._set_form_read_only(True)
        self.view_lineage_button.setVisible(True)
        self.record_button.setText(
            "ACTION AUTHORISED"
        )
        self.record_button.setEnabled(False)

    def _open_lineage_dialog(self):
        action = self._selected_action

        if self.project is None or action is None:
            return

        dialog = ImprovementLineageDialog(
            self.project,
            action,
            self,
        )
        dialog.exec()

    @staticmethod
    def _allowed_status_transitions(status):
        """
        Return deliberately permitted lifecycle transitions.

        Completed and Cancelled are terminal in GREEN 7-6A.
        Completion evidence is handled separately in GREEN 7-6B.
        """
        transitions = {
            ActionStatus.NOT_STARTED: [
                ActionStatus.IN_PROGRESS,
                ActionStatus.CANCELLED,
            ],
            ActionStatus.IN_PROGRESS: [
                ActionStatus.BLOCKED,
                ActionStatus.COMPLETED,
                ActionStatus.CANCELLED,
            ],
            ActionStatus.BLOCKED: [
                ActionStatus.IN_PROGRESS,
                ActionStatus.CANCELLED,
            ],
            ActionStatus.COMPLETED: [],
            ActionStatus.CANCELLED: [],
        }

        return transitions.get(status, [])

    def _reset_status_change_controls(self):
        self._reset_completion_controls()
        self.lifecycle_record_detail.clear()
        self.lifecycle_record_detail.setVisible(False)

        self.change_status_button.setVisible(False)

        self.next_status_input.clear()
        self.next_status_input.setVisible(False)

        self.status_rationale_input.clear()
        self.status_rationale_input.setVisible(False)

        self.status_changed_by_input.clear()
        self.status_changed_by_input.setVisible(False)

        self.record_status_change_button.setVisible(False)
        self.record_status_change_button.setEnabled(False)

    def _show_lifecycle_state(self, action):
        self._reset_status_change_controls()

        transition = getattr(
            action,
            "_latest_status_transition",
            None,
        )

        if transition:
            detail_lines = [
                f"Previous status: {transition.get('from', '-')}",
                f"Changed by: {transition.get('changed_by', '-')}",
                f"Recorded: {transition.get('recorded_at', '-')}",
                f"Rationale: {transition.get('rationale', '-')}",
            ]
            self.lifecycle_record_detail.setText(
                "\n".join(detail_lines)
            )
            self.lifecycle_record_detail.setVisible(True)

        allowed = self._allowed_status_transitions(
            action.status
        )

        if action.status == ActionStatus.IN_PROGRESS:
            allowed = [
                status
                for status in allowed
                if status != ActionStatus.COMPLETED
            ]
            self._show_completion_controls(action)

        if action.status == ActionStatus.COMPLETED:
            verification = self._find_verification_for_action(
                action
            )
            self.verify_improvement_button.setVisible(
                verification is None
            )
            if verification is not None:
                self._show_verification_record(
                    verification
                )

        self.change_status_button.setVisible(
            bool(allowed)
        )

    def _start_status_change(self):
        action = self._selected_action
        if action is None:
            return

        allowed = self._allowed_status_transitions(
            action.status
        )
        if action.status == ActionStatus.IN_PROGRESS:
            allowed = [
                status
                for status in allowed
                if status != ActionStatus.COMPLETED
            ]
        if not allowed:
            return

        self.change_status_button.setVisible(False)

        self.next_status_input.clear()
        self.next_status_input.addItem(
            "Select next status...",
            None,
        )
        for status in allowed:
            self.next_status_input.addItem(
                status.value,
                status,
            )
        self.next_status_input.setVisible(True)

        self.status_rationale_input.clear()
        self.status_rationale_input.setVisible(True)

        self.status_changed_by_input.clear()
        self.status_changed_by_input.setVisible(True)

        self.record_status_change_button.setVisible(True)
        self._update_status_change_button()

    def _update_status_change_button(self, *_):
        action = self._selected_action

        if action is None:
            self.record_status_change_button.setEnabled(False)
            return

        next_status = self.next_status_input.currentData()

        enabled = bool(
            next_status is not None
            and next_status
            in self._allowed_status_transitions(action.status)
            and self.status_rationale_input
            .toPlainText()
            .strip()
            and self.status_changed_by_input
            .text()
            .strip()
        )

        self.record_status_change_button.setEnabled(
            enabled
        )

    def _record_status_change(self):
        action = self._selected_action

        if action is None:
            return

        next_status = self.next_status_input.currentData()
        rationale = (
            self.status_rationale_input
            .toPlainText()
            .strip()
        )
        changed_by = (
            self.status_changed_by_input
            .text()
            .strip()
        )

        if (
            next_status is None
            or next_status == ActionStatus.COMPLETED
            or next_status
            not in self._allowed_status_transitions(action.status)
            or not rationale
            or not changed_by
        ):
            return

        from datetime import datetime

        previous_status = action.status
        action.status = next_status

        # GREEN 7-6A keeps the latest transition as factual lifecycle
        # metadata without changing the core dataclass yet. GREEN 7-6B
        # will formalise completion evidence and history persistence.
        action._latest_status_transition = {
            "from": previous_status.value,
            "to": next_status.value,
            "rationale": rationale,
            "changed_by": changed_by,
            "recorded_at": datetime.now().isoformat(
                timespec="seconds"
            ),
        }

        self.lifecycle_label.setText(
            action.status.value
        )

        self.action_status_changed.emit(action)
        self._refresh_improvement_overview()

        for row in range(
            self.actions_list.count()
        ):
            item = self.actions_list.item(row)
            if (
                item.data(Qt.ItemDataRole.UserRole)
                == action.action_id
            ):
                item.setText(
                    self._action_display_text(action)
                )
                break

        self._show_lifecycle_state(action)
        self._apply_action_filter()

    def _reset_completion_controls(self):
        self.complete_action_button.setVisible(False)
        self.verify_improvement_button.setVisible(False)
        self._hide_verification_record()

    def _hide_verification_record(self):
        self.verification_outcome_label.clear()
        self.verification_follow_up_label.clear()
        self.follow_up_action_button.setVisible(False)
        self.verification_record_frame.setVisible(False)

    def _find_verification_for_action(self, action):
        if self.project is None:
            return None

        for verification in getattr(
            self.project,
            "improvement_verifications",
            [],
        ):
            if verification.related_action_id == action.action_id:
                return verification

        return None

    def _show_verification_record(self, verification):
        if verification is None:
            self._hide_verification_record()
            return

        outcome = getattr(
            verification.outcome,
            "value",
            str(verification.outcome),
        )
        follow_up_state = verification.follow_up_state()

        self.verification_outcome_label.setText(
            f"Outcome: {outcome}"
        )
        self.verification_follow_up_label.setText(
            f"Follow-up state: {follow_up_state.value}"
        )
        self.follow_up_action_button.setVisible(
            follow_up_state.value == "Further Improvement Required"
        )
        self.verification_record_frame.setVisible(True)

    def _prepare_follow_up_action(self):
        source_action = self._selected_action

        if self.project is None or source_action is None:
            return

        verification = self._find_verification_for_action(
            source_action
        )
        if verification is None:
            return

        follow_up_state = verification.follow_up_state()
        if follow_up_state.value != "Further Improvement Required":
            return

        recommendation_ids = list(
            source_action.related_recommendation_ids
        )

        self._prepare_new_action()
        self._pending_follow_up_verification_id = (
            verification.verification_id
        )

        self.title_input.setText(
            f"Follow-up: {source_action.title or 'Improvement action'}"
        )
        self.description_input.setPlainText(
            "Follow-up improvement action arising from verification of: "
            f"{source_action.title or 'Untitled action'}"
        )

        self.recommendations_list.blockSignals(True)
        for row in range(self.recommendations_list.count()):
            item = self.recommendations_list.item(row)
            recommendation_id = item.data(
                Qt.ItemDataRole.UserRole
            )
            item.setCheckState(
                Qt.CheckState.Checked
                if recommendation_id in recommendation_ids
                else Qt.CheckState.Unchecked
            )
        self.recommendations_list.blockSignals(False)

        self._populate_related_findings()
        self._update_record_button()
        self.review_scroll_area.verticalScrollBar().setValue(0)

    def _open_verification_record_dialog(self):
        action = self._selected_action

        if action is None:
            return

        verification = self._find_verification_for_action(
            action
        )
        if verification is None:
            return

        dialog = VerificationRecordDialog(
            self.project,
            verification,
            self,
        )
        dialog.exec()

    def _show_completion_controls(self, action):
        self.complete_action_button.setVisible(
            action.status == ActionStatus.IN_PROGRESS
        )

    def _open_completion_dialog(self):
        action = self._selected_action

        if (
            action is None
            or action.status != ActionStatus.IN_PROGRESS
        ):
            return

        dialog = ActionCompletionDialog(
            self.project,
            action,
            self,
        )

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        completion_notes = dialog.completion_notes()
        completed_by = dialog.completed_by()

        if not completion_notes or not completed_by:
            return

        action.completion_notes = completion_notes
        action.completed_by = completed_by
        action.completion_evidence_ids = (
            dialog.evidence_ids()
        )
        action.status = ActionStatus.COMPLETED
        action.mark_completed_now()

        action._latest_status_transition = {
            "from": ActionStatus.IN_PROGRESS.value,
            "to": ActionStatus.COMPLETED.value,
            "rationale": completion_notes,
            "changed_by": completed_by,
            "recorded_at": action.completed_at,
        }

        self.lifecycle_label.setText(
            action.status.value
        )

        self.action_status_changed.emit(action)

        for row in range(
            self.actions_list.count()
        ):
            item = self.actions_list.item(row)
            if (
                item.data(Qt.ItemDataRole.UserRole)
                == action.action_id
            ):
                item.setText(
                    self._action_display_text(action)
                )
                break

        self._show_lifecycle_state(action)
        self._refresh_improvement_overview()
        self._apply_action_filter()

    def _action_has_verification(self, action):
        if self.project is None:
            return False

        return any(
            verification.related_action_id == action.action_id
            for verification in getattr(
                self.project,
                "improvement_verifications",
                [],
            )
        )

    def _open_verification_dialog(self):
        action = self._selected_action

        if (
            self.project is None
            or action is None
            or action.status != ActionStatus.COMPLETED
            or self._action_has_verification(action)
        ):
            return

        dialog = ImprovementVerificationDialog(
            self.project,
            action,
            self,
        )

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        outcome = dialog.outcome()
        rationale = dialog.rationale()
        assessed_by = dialog.assessed_by()
        assessment_authority = (
            dialog.assessment_authority()
        )

        if (
            outcome is None
            or not rationale
            or not assessed_by
            or not assessment_authority
        ):
            return

        verification = ImprovementVerification(
            related_action_id=action.action_id,
            related_finding_ids=list(
                action.related_finding_ids
            ),
            related_evidence_ids=dialog.evidence_ids(),
            outcome=outcome,
            rationale=rationale,
            assessed_by=assessed_by,
            assessment_authority=assessment_authority,
        )
        verification.mark_recorded_now()

        self.project.add_improvement_verification(
            verification
        )
        self.verification_recorded.emit(verification)
        self._refresh_improvement_overview()

        self.verify_improvement_button.setVisible(False)
        self._show_verification_record(verification)
        self._apply_action_filter()

    def _set_form_read_only(self, read_only):
        self.title_input.setReadOnly(read_only)
        self.description_input.setReadOnly(
            read_only
        )
        self.owner_input.setReadOnly(read_only)
        self.priority_input.setEnabled(
            not read_only
        )
        self.target_date_input.setEnabled(
            not read_only
        )
        self.authorised_by_input.setReadOnly(
            read_only
        )

        for row in range(
            self.recommendations_list.count()
        ):
            item = self.recommendations_list.item(row)
            flags = item.flags()
            if read_only:
                item.setFlags(
                    flags
                    & ~Qt.ItemFlag.ItemIsEnabled
                )
            else:
                item.setFlags(
                    flags
                    | Qt.ItemFlag.ItemIsEnabled
                )

        for row in range(
            self.findings_list.count()
        ):
            item = self.findings_list.item(row)
            flags = item.flags()
            if read_only:
                item.setFlags(
                    flags
                    & ~Qt.ItemFlag.ItemIsEnabled
                )

    def _update_record_button(self, *_):
        if self._selected_action is not None:
            self.record_button.setEnabled(False)
            return

        enabled = bool(
            self.title_input.text().strip()
            and self.description_input
            .toPlainText()
            .strip()
            and self._selected_recommendation_id()
            and self.owner_input.text().strip()
            and self.authorised_by_input
            .text()
            .strip()
        )

        self.record_button.setEnabled(
            enabled
        )

    def _record_action(self):
        if (
            self.project is None
            or self._selected_action is not None
        ):
            return

        recommendation_id = (
            self._selected_recommendation_id()
        )
        recommendation = self._find_recommendation(
            recommendation_id
        )

        if recommendation is None:
            return

        if recommendation.disposition not in {
            RecommendationDisposition.ACCEPTED,
            RecommendationDisposition.ACCEPTED_IN_PART,
        }:
            return

        title = self.title_input.text().strip()
        description = (
            self.description_input
            .toPlainText()
            .strip()
        )
        owner = self.owner_input.text().strip()
        authorised_by = (
            self.authorised_by_input
            .text()
            .strip()
        )

        if (
            not title
            or not description
            or not owner
            or not authorised_by
        ):
            return

        action = ImprovementAction(
            title=title,
            description=description,
            related_recommendation_ids=[
                recommendation.recommendation_id
            ],
            related_finding_ids=list(
                recommendation.related_finding_ids
            ),
            related_verification_ids=(
                [self._pending_follow_up_verification_id]
                if self._pending_follow_up_verification_id
                else []
            ),
            owner=owner,
            priority=self.priority_input.currentData(),
            target_date=(
                self.target_date_input.date()
                .toString("yyyy-MM-dd")
            ),
            status=ActionStatus.NOT_STARTED,
            authorised_by=authorised_by,
        )
        action.mark_authorised_now()

        self.action_recorded.emit(action)

        if any(
            existing.action_id == action.action_id
            for existing in getattr(
                self.project,
                "improvement_actions",
                [],
            )
        ):
            self.refresh()

            for row in range(
                self.actions_list.count()
            ):
                item = self.actions_list.item(row)
                if (
                    item.data(
                        Qt.ItemDataRole.UserRole
                    )
                    == action.action_id
                ):
                    self.actions_list.setCurrentRow(
                        row
                    )
                    break
        else:
            self.status_label.setText(
                "Action Status: AUTHORISED "
                "- awaiting project refresh"
            )
            self._set_form_read_only(True)
            self.record_button.setText(
                "ACTION AUTHORISED"
            )
            self.record_button.setEnabled(False)
