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

from core.improvement.recommendation import (
    Recommendation,
    RecommendationDisposition,
    RecommendationType,
)


class RecommendationsPanel(QWidget):
    """
    Recommendation review workspace.

    Records professional advice arising from one or more findings.
    A recommendation does not itself authorise an improvement action.
    """

    recommendation_recorded = Signal(object)
    recommendation_dispositioned = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.project = None
        self._selected_recommendation = None

        self._build_ui()

        self.recommendations_list.currentRowChanged.connect(
            self._show_selected_recommendation
        )
        self.title_input.textChanged.connect(
            self._update_record_button
        )
        self.description_input.textChanged.connect(
            self._update_record_button
        )
        self.recommended_by_input.textChanged.connect(
            self._update_record_button
        )
        self.findings_list.itemChanged.connect(
            self._update_record_button
        )
        self.record_button.clicked.connect(
            self._record_recommendation
        )
        self.new_button.clicked.connect(
            self._prepare_new_recommendation
        )
        self.start_disposition_button.clicked.connect(
            self._start_disposition_review
        )
        self.disposition_input.currentIndexChanged.connect(
            self._update_disposition_button
        )
        self.disposition_rationale_input.textChanged.connect(
            self._update_disposition_button
        )
        self.disposition_by_input.textChanged.connect(
            self._update_disposition_button
        )
        self.disposition_authority_input.textChanged.connect(
            self._update_disposition_button
        )
        self.record_disposition_button.clicked.connect(
            self._record_disposition
        )

    def _build_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # -------------------------------------------------
        # Recorded recommendations
        # -------------------------------------------------

        left_frame = QFrame()
        left_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )
        left_layout = QVBoxLayout(left_frame)

        left_heading = QLabel("RECORDED RECOMMENDATIONS")
        left_heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        guidance = QLabel(
            "Recommendations record professional advice arising from "
            "exercise findings. Select a recommendation to inspect its "
            "immutable record."
        )
        guidance.setWordWrap(True)

        self.recommendations_list = QListWidget()

        self.new_button = QPushButton(
            "NEW RECOMMENDATION"
        )

        left_layout.addWidget(left_heading)
        left_layout.addWidget(guidance)
        left_layout.addWidget(
            self.recommendations_list
        )
        left_layout.addWidget(self.new_button)

        # -------------------------------------------------
        # Recommendation detail / creation
        # -------------------------------------------------

        right_frame = QFrame()
        right_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )
        right_layout = QVBoxLayout(right_frame)

        heading = QLabel("RECOMMENDATION REVIEW")
        heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.status_label = QLabel(
            "Recommendation Status: NEW RECOMMENDATION"
        )
        self.status_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText(
            "Recommendation title"
        )

        self.type_input = QComboBox()
        for recommendation_type in RecommendationType:
            self.type_input.addItem(
                recommendation_type.value,
                recommendation_type,
            )

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText(
            "Record the professional advice arising from the finding. "
            "Do not authorise an action here."
        )
        self.description_input.setMinimumHeight(120)

        self.recommended_by_input = QLineEdit()
        self.recommended_by_input.setPlaceholderText(
            "Recommended by - name / role"
        )

        provenance_heading = QLabel(
            "RELATED FINDINGS"
        )
        provenance_heading.setStyleSheet(
            "font-weight: bold;"
        )

        provenance_note = QLabel(
            "Select the recorded findings that gave rise to this "
            "recommendation. These links preserve provenance."
        )
        provenance_note.setWordWrap(True)

        self.findings_list = QListWidget()
        self.findings_list.setSelectionMode(
            QListWidget.SelectionMode.NoSelection
        )
        self.findings_list.setMinimumHeight(130)

        disposition_heading = QLabel(
            "AUTHORISED DISPOSITION"
        )
        disposition_heading.setStyleSheet(
            "font-weight: bold;"
        )

        disposition_note = QLabel(
            "A recorded recommendation remains professional advice until "
            "an authorised person records its disposition. Disposition does "
            "not itself create or authorise an improvement action."
        )
        disposition_note.setWordWrap(True)
        disposition_note.setStyleSheet(
            "font-style: italic;"
        )

        self.disposition_label = QLabel(
            RecommendationDisposition.NOT_REVIEWED.value
        )
        self.disposition_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.disposition_record_detail = QLabel("")
        self.disposition_record_detail.setWordWrap(True)
        self.disposition_record_detail.setVisible(False)

        self.start_disposition_button = QPushButton(
            "REVIEW RECOMMENDATION DISPOSITION"
        )
        self.start_disposition_button.setVisible(False)

        self.disposition_input = QComboBox()
        self.disposition_input.addItem(
            "Select disposition...",
            None,
        )
        for disposition in RecommendationDisposition:
            if disposition != RecommendationDisposition.NOT_REVIEWED:
                self.disposition_input.addItem(
                    disposition.value,
                    disposition,
                )
        self.disposition_input.setVisible(False)

        self.disposition_rationale_input = QTextEdit()
        self.disposition_rationale_input.setPlaceholderText(
            "Record the professional rationale for this disposition."
        )
        self.disposition_rationale_input.setMinimumHeight(90)
        self.disposition_rationale_input.setVisible(False)

        self.disposition_by_input = QLineEdit()
        self.disposition_by_input.setPlaceholderText(
            "Disposition by - name / role"
        )
        self.disposition_by_input.setVisible(False)

        self.disposition_authority_input = QLineEdit()
        self.disposition_authority_input.setPlaceholderText(
            "Disposition authority / role"
        )
        self.disposition_authority_input.setVisible(False)

        self.record_disposition_button = QPushButton(
            "RECORD AUTHORISED DISPOSITION"
        )
        self.record_disposition_button.setEnabled(False)
        self.record_disposition_button.setVisible(False)

        note = QLabel(
            "Exercise Director records professional advice and its "
            "relationship to findings. A recommendation does not itself "
            "create or authorise an improvement action."
        )
        note.setWordWrap(True)
        note.setStyleSheet(
            "font-style: italic;"
        )

        self.record_button = QPushButton(
            "RECORD RECOMMENDATION"
        )
        self.record_button.setEnabled(False)

        right_layout.addWidget(heading)
        right_layout.addWidget(self.status_label)
        right_layout.addWidget(QLabel("Title"))
        right_layout.addWidget(self.title_input)
        right_layout.addWidget(
            QLabel("Recommendation Type")
        )
        right_layout.addWidget(self.type_input)
        right_layout.addWidget(QLabel("Description"))
        right_layout.addWidget(
            self.description_input
        )
        right_layout.addWidget(
            QLabel("Recommended By")
        )
        right_layout.addWidget(
            self.recommended_by_input
        )
        right_layout.addWidget(provenance_heading)
        right_layout.addWidget(provenance_note)
        right_layout.addWidget(self.findings_list)
        right_layout.addWidget(disposition_heading)
        right_layout.addWidget(disposition_note)
        right_layout.addWidget(self.disposition_label)
        right_layout.addWidget(self.disposition_record_detail)
        right_layout.addWidget(self.start_disposition_button)
        right_layout.addWidget(self.disposition_input)
        right_layout.addWidget(self.disposition_rationale_input)
        right_layout.addWidget(self.disposition_by_input)
        right_layout.addWidget(self.disposition_authority_input)
        right_layout.addWidget(self.record_disposition_button)
        right_layout.addWidget(note)
        right_layout.addWidget(self.record_button)

        main_layout.addWidget(left_frame, 4)
        main_layout.addWidget(right_frame, 6)

    def set_project(self, project):
        self.project = project
        self.refresh()

    def refresh(self):
        self.recommendations_list.clear()
        self._populate_findings()
        self._prepare_new_recommendation()

        if self.project is None:
            return

        for recommendation in getattr(
            self.project,
            "recommendations",
            [],
        ):
            item = QListWidgetItem(
                self._recommendation_display_text(
                    recommendation
                )
            )
            item.setData(
                Qt.ItemDataRole.UserRole,
                recommendation.recommendation_id,
            )
            self.recommendations_list.addItem(item)

    @staticmethod
    def _recommendation_display_text(
        recommendation,
    ):
        title = (
            recommendation.title
            or "Untitled recommendation"
        )
        recommendation_type = getattr(
            recommendation.recommendation_type,
            "value",
            str(recommendation.recommendation_type),
        )
        disposition = getattr(
            recommendation.disposition,
            "value",
            str(recommendation.disposition),
        )

        return (
            f"{recommendation_type} | {title} | "
            f"{disposition}"
        )

    def _populate_findings(self):
        self.findings_list.clear()

        if self.project is None:
            return

        for finding in getattr(
            self.project,
            "findings",
            [],
        ):
            finding_type = getattr(
                getattr(
                    finding,
                    "finding_type",
                    None,
                ),
                "value",
                "Finding",
            )
            title = (
                getattr(
                    finding,
                    "title",
                    "",
                )
                or "Untitled finding"
            )
            finding_id = getattr(
                finding,
                "finding_id",
                "",
            )

            item = QListWidgetItem(
                f"{finding_type} | {title}"
            )
            item.setData(
                Qt.ItemDataRole.UserRole,
                finding_id,
            )
            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
            )
            item.setCheckState(
                Qt.CheckState.Unchecked
            )
            self.findings_list.addItem(item)

    def _find_recommendation(
        self,
        recommendation_id,
    ):
        if self.project is None or not recommendation_id:
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

    def _show_selected_recommendation(
        self,
        row,
    ):
        if row < 0:
            return

        item = self.recommendations_list.item(row)
        if item is None:
            return

        recommendation = self._find_recommendation(
            item.data(Qt.ItemDataRole.UserRole)
        )
        if recommendation is None:
            return

        self._selected_recommendation = recommendation

        self.status_label.setText(
            "Recommendation Status: "
            "RECOMMENDATION RECORDED"
        )
        self.title_input.setText(
            recommendation.title
        )

        type_index = self.type_input.findData(
            recommendation.recommendation_type
        )
        if type_index >= 0:
            self.type_input.setCurrentIndex(
                type_index
            )

        self.description_input.setPlainText(
            recommendation.description
        )
        self.recommended_by_input.setText(
            recommendation.recommended_by
        )
        self.disposition_label.setText(
            recommendation.disposition.value
        )
        self._show_disposition_state(
            recommendation
        )

        self._set_checked_ids(
            self.findings_list,
            recommendation.related_finding_ids,
        )

        self._set_form_read_only(True)
        self.record_button.setText(
            "RECOMMENDATION RECORDED"
        )
        self.record_button.setEnabled(False)

    def _prepare_new_recommendation(self):
        self._selected_recommendation = None

        self.recommendations_list.blockSignals(
            True
        )
        self.recommendations_list.clearSelection()
        self.recommendations_list.setCurrentRow(-1)
        self.recommendations_list.blockSignals(
            False
        )

        self.status_label.setText(
            "Recommendation Status: "
            "NEW RECOMMENDATION"
        )
        self.title_input.clear()

        default_index = self.type_input.findData(
            RecommendationType.IMPROVEMENT
        )
        self.type_input.setCurrentIndex(
            default_index
            if default_index >= 0
            else 0
        )

        self.description_input.clear()
        self.recommended_by_input.clear()
        self.disposition_label.setText(
            RecommendationDisposition.NOT_REVIEWED.value
        )
        self._reset_disposition_controls()

        self._set_checked_ids(
            self.findings_list,
            [],
        )

        self._set_form_read_only(False)
        self.record_button.setText(
            "RECORD RECOMMENDATION"
        )
        self._update_record_button()

    def _reset_disposition_controls(self):
        self.disposition_record_detail.clear()
        self.disposition_record_detail.setVisible(False)
        self.start_disposition_button.setVisible(False)

        self.disposition_input.setCurrentIndex(0)
        self.disposition_input.setVisible(False)

        self.disposition_rationale_input.clear()
        self.disposition_rationale_input.setVisible(False)

        self.disposition_by_input.clear()
        self.disposition_by_input.setVisible(False)

        self.disposition_authority_input.clear()
        self.disposition_authority_input.setVisible(False)

        self.record_disposition_button.setVisible(False)
        self.record_disposition_button.setEnabled(False)

    def _show_disposition_state(self, recommendation):
        self._reset_disposition_controls()

        if (
            recommendation.disposition
            == RecommendationDisposition.NOT_REVIEWED
        ):
            self.start_disposition_button.setVisible(True)
            return

        detail_lines = []

        if recommendation.disposition_by:
            detail_lines.append(
                f"Disposition by: {recommendation.disposition_by}"
            )

        if recommendation.disposition_authority:
            detail_lines.append(
                "Authority: "
                f"{recommendation.disposition_authority}"
            )

        if recommendation.disposition_at:
            detail_lines.append(
                f"Recorded: {recommendation.disposition_at}"
            )

        if recommendation.disposition_rationale:
            detail_lines.append(
                "Rationale: "
                f"{recommendation.disposition_rationale}"
            )

        self.disposition_record_detail.setText(
            "\n".join(detail_lines)
        )
        self.disposition_record_detail.setVisible(
            bool(detail_lines)
        )

    def _start_disposition_review(self):
        recommendation = self._selected_recommendation

        if recommendation is None:
            return

        if (
            recommendation.disposition
            != RecommendationDisposition.NOT_REVIEWED
        ):
            return

        self.start_disposition_button.setVisible(False)

        self.disposition_input.setCurrentIndex(0)
        self.disposition_input.setVisible(True)

        self.disposition_rationale_input.clear()
        self.disposition_rationale_input.setVisible(True)

        self.disposition_by_input.clear()
        self.disposition_by_input.setVisible(True)

        self.disposition_authority_input.clear()
        self.disposition_authority_input.setVisible(True)

        self.record_disposition_button.setVisible(True)
        self._update_disposition_button()

    def _update_disposition_button(self, *_):
        recommendation = self._selected_recommendation

        if recommendation is None:
            self.record_disposition_button.setEnabled(False)
            return

        if (
            recommendation.disposition
            != RecommendationDisposition.NOT_REVIEWED
        ):
            self.record_disposition_button.setEnabled(False)
            return

        enabled = bool(
            self.disposition_input.currentData() is not None
            and self.disposition_rationale_input
            .toPlainText()
            .strip()
            and self.disposition_by_input
            .text()
            .strip()
            and self.disposition_authority_input
            .text()
            .strip()
        )

        self.record_disposition_button.setEnabled(
            enabled
        )

    def _record_disposition(self):
        recommendation = self._selected_recommendation

        if recommendation is None:
            return

        if (
            recommendation.disposition
            != RecommendationDisposition.NOT_REVIEWED
        ):
            return

        disposition = self.disposition_input.currentData()
        rationale = (
            self.disposition_rationale_input
            .toPlainText()
            .strip()
        )
        disposition_by = (
            self.disposition_by_input
            .text()
            .strip()
        )
        authority = (
            self.disposition_authority_input
            .text()
            .strip()
        )

        if (
            disposition is None
            or not rationale
            or not disposition_by
            or not authority
        ):
            return

        recommendation.disposition = disposition
        recommendation.disposition_rationale = rationale
        recommendation.disposition_by = disposition_by
        recommendation.disposition_authority = authority
        recommendation.mark_dispositioned_now()

        self.recommendation_dispositioned.emit(
            recommendation
        )

        self.disposition_label.setText(
            recommendation.disposition.value
        )
        self._show_disposition_state(
            recommendation
        )

        self.recommendations_list.blockSignals(True)

        for row in range(
            self.recommendations_list.count()
        ):
            item = self.recommendations_list.item(row)

            if (
                item.data(Qt.ItemDataRole.UserRole)
                == recommendation.recommendation_id
            ):
                item.setText(
                    self._recommendation_display_text(
                        recommendation
                    )
                )
                break

        self.recommendations_list.blockSignals(False)

    def _set_form_read_only(
        self,
        read_only,
    ):
        self.title_input.setReadOnly(
            read_only
        )
        self.type_input.setEnabled(
            not read_only
        )
        self.description_input.setReadOnly(
            read_only
        )
        self.recommended_by_input.setReadOnly(
            read_only
        )
        self._set_checkable_enabled(
            self.findings_list,
            not read_only,
        )

    @staticmethod
    def _set_checkable_enabled(
        list_widget,
        enabled,
    ):
        for row in range(
            list_widget.count()
        ):
            item = list_widget.item(row)
            flags = item.flags()

            if enabled:
                item.setFlags(
                    flags
                    | Qt.ItemFlag.ItemIsEnabled
                )
            else:
                item.setFlags(
                    flags
                    & ~Qt.ItemFlag.ItemIsEnabled
                )

    @staticmethod
    def _set_checked_ids(
        list_widget,
        wanted_ids,
    ):
        wanted = set(
            wanted_ids or []
        )

        for row in range(
            list_widget.count()
        ):
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
    def _checked_ids(
        list_widget,
    ):
        values = []

        for row in range(
            list_widget.count()
        ):
            item = list_widget.item(row)

            if (
                item.checkState()
                == Qt.CheckState.Checked
            ):
                item_id = item.data(
                    Qt.ItemDataRole.UserRole
                )
                if item_id:
                    values.append(
                        item_id
                    )

        return values

    def _update_record_button(
        self,
        *_,
    ):
        if (
            self._selected_recommendation
            is not None
        ):
            self.record_button.setEnabled(
                False
            )
            return

        has_finding = bool(
            self._checked_ids(
                self.findings_list
            )
        )

        enabled = bool(
            self.title_input.text().strip()
            and self.description_input
            .toPlainText()
            .strip()
            and self.recommended_by_input
            .text()
            .strip()
            and has_finding
        )

        self.record_button.setEnabled(
            enabled
        )

    def _record_recommendation(self):
        if self.project is None:
            return

        if (
            self._selected_recommendation
            is not None
        ):
            return

        title = self.title_input.text().strip()
        description = (
            self.description_input
            .toPlainText()
            .strip()
        )
        recommended_by = (
            self.recommended_by_input
            .text()
            .strip()
        )
        finding_ids = self._checked_ids(
            self.findings_list
        )

        if (
            not title
            or not description
            or not recommended_by
            or not finding_ids
        ):
            return

        recommendation = Recommendation(
            title=title,
            recommendation_type=(
                self.type_input.currentData()
            ),
            description=description,
            related_finding_ids=finding_ids,
            disposition=(
                RecommendationDisposition.NOT_REVIEWED
            ),
            recommended_by=recommended_by,
        )
        recommendation.mark_recorded_now()

        self.recommendation_recorded.emit(
            recommendation
        )

        if any(
            existing.recommendation_id
            == recommendation.recommendation_id
            for existing in getattr(
                self.project,
                "recommendations",
                [],
            )
        ):
            self.refresh()

            for row in range(
                self.recommendations_list.count()
            ):
                item = self.recommendations_list.item(row)
                if (
                    item.data(
                        Qt.ItemDataRole.UserRole
                    )
                    == recommendation.recommendation_id
                ):
                    self.recommendations_list.setCurrentRow(
                        row
                    )
                    break
        else:
            self.status_label.setText(
                "Recommendation Status: RECORDED "
                "- awaiting project refresh"
            )
            self._set_form_read_only(True)
            self.record_button.setText(
                "RECOMMENDATION RECORDED"
            )
            self.record_button.setEnabled(False)
