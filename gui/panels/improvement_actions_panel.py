from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
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

from core.improvement.action import (
    ActionPriority,
    ActionStatus,
    ImprovementAction,
)
from core.improvement.recommendation import (
    RecommendationDisposition,
)


class ImprovementActionsPanel(QWidget):
    """
    Records authorised improvement actions arising from accepted
    recommendations.

    An accepted recommendation does not automatically become an action.
    The user must deliberately create and authorise the action.
    """

    action_recorded = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.project = None
        self._selected_action = None

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

        self.actions_list = QListWidget()

        self.new_button = QPushButton(
            "NEW IMPROVEMENT ACTION"
        )

        left_layout.addWidget(left_heading)
        left_layout.addWidget(left_note)
        left_layout.addWidget(self.actions_list)
        left_layout.addWidget(self.new_button)

        # -------------------------------------------------
        # Action creation / inspection
        # -------------------------------------------------

        right_frame = QFrame()
        right_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )
        right_layout = QVBoxLayout(right_frame)

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
            "GREEN 7-5A records creation and authorisation only. "
            "Lifecycle changes and completion evidence remain separate "
            "controlled steps."
        )
        lifecycle_note.setWordWrap(True)
        lifecycle_note.setStyleSheet(
            "font-style: italic;"
        )

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
        right_layout.addWidget(self.record_button)

        main_layout.addWidget(left_frame, 4)
        main_layout.addWidget(right_frame, 6)

    def set_project(self, project):
        self.project = project
        self.refresh()

    def refresh(self):
        self.actions_list.clear()
        self._populate_recommendations()
        self._prepare_new_action()

        if self.project is None:
            return

        for action in getattr(
            self.project,
            "improvement_actions",
            [],
        ):
            item = QListWidgetItem(
                self._action_display_text(action)
            )
            item.setData(
                Qt.ItemDataRole.UserRole,
                action.action_id,
            )
            self.actions_list.addItem(item)

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

        self.recommendations_list.blockSignals(True)
        for row in range(
            self.recommendations_list.count()
        ):
            self.recommendations_list.item(row).setCheckState(
                Qt.CheckState.Unchecked
            )
        self.recommendations_list.blockSignals(False)

        self.findings_list.clear()
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
        self.record_button.setText(
            "ACTION AUTHORISED"
        )
        self.record_button.setEnabled(False)

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
