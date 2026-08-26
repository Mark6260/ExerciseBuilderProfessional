from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)


class DesignTracePanel(QWidget):
    """
    Read-only view of the project's design provenance.

    This panel presents DesignTraceRecord objects but does
    not modify trace records or the authoritative design.
    """

    def __init__(self):
        super().__init__()

        self.project = None
        self.trace_records = []

        main_layout = QVBoxLayout(self)

        heading = QLabel("Design Trace")
        heading.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )
        main_layout.addWidget(heading)

        description = QLabel(
            "Review the recorded history of assisted "
            "exercise design decisions."
        )
        description.setWordWrap(True)
        main_layout.addWidget(description)

        content = QHBoxLayout()
        main_layout.addLayout(content, 1)

        history_group = QGroupBox("History")
        history_layout = QVBoxLayout(
            history_group
        )

        self.trace_tree = QTreeWidget()
        self.trace_tree.setColumnCount(1)
        self.trace_tree.setHeaderLabels(
            ["Design Decision History"]
        )

        self.trace_tree.currentItemChanged.connect(
            self._trace_selected
        )

        history_layout.addWidget(
            self.trace_tree
        )

        content.addWidget(
            history_group,
            2,
        )

        detail_group = QGroupBox(
            "Decision Record"
        )
        detail_layout = QVBoxLayout(
            detail_group
        )

        self.detail_label = QLabel(
            "Select a trace record to review "
            "its design provenance."
        )
        self.detail_label.setWordWrap(True)
        self.detail_label.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.detail_scroll = QScrollArea()
        self.detail_scroll.setWidgetResizable(
            True
        )
        self.detail_scroll.setFrameShape(
            QScrollArea.Shape.NoFrame
        )
        self.detail_scroll.setWidget(
            self.detail_label
        )

        detail_layout.addWidget(
            self.detail_scroll,
            1,
        )

        content.addWidget(
            detail_group,
            3,
        )

    def set_project(self, project):
        self.project = project
        self.refresh()

    def refresh(self):
        self.trace_tree.clear()
        self.trace_records = []

        if self.project is None:
            self.detail_label.setText(
                "No project is currently loaded."
            )
            return

        self.trace_records = list(
            self.project.design_trace_records
        )

        if not self.trace_records:
            self.detail_label.setText(
                "No design trace records are "
                "currently available."
            )
            return

        objective_groups = {}
        standalone_records = []

        for record in self.trace_records:
            if not record.proposal_id:
                standalone_records.append(
                    record
                )
                continue

            objective_title = (
                record.objective_title
                or "Unspecified Objective"
            )

            objective_groups.setdefault(
                objective_title,
                {},
            )

            objective_groups[
                objective_title
            ].setdefault(
                record.proposal_id,
                [],
            ).append(record)

        for (
            objective_title,
            proposal_groups,
        ) in objective_groups.items():
            objective_item = QTreeWidgetItem(
                [objective_title]
            )

            objective_item.setData(
                0,
                Qt.ItemDataRole.UserRole,
                None,
            )

            self.trace_tree.addTopLevelItem(
                objective_item
            )

            for (
                proposal_id,
                records,
            ) in proposal_groups.items():
                outcome = self._proposal_outcome(
                    records
                )

                timestamp = self._proposal_timestamp(
                    records
                )

                case_text = outcome

                if timestamp:
                    case_text += (
                        f" — {timestamp}"
                    )

                case_item = QTreeWidgetItem(
                    objective_item,
                    [case_text],
                )

                case_item.setData(
                    0,
                    Qt.ItemDataRole.UserRole,
                    None,
                )

                case_item.setToolTip(
                    0,
                    f"Proposal ID: {proposal_id}",
                )

                for record in records:
                    event_text = (
                        record.event_type.value
                    )

                    if record.recorded_at:
                        event_text += (
                            " — "
                            f"{self._format_timestamp(record.recorded_at)}"
                        )

                    event_item = QTreeWidgetItem(
                        case_item,
                        [event_text],
                    )

                    event_item.setData(
                        0,
                        Qt.ItemDataRole.UserRole,
                        record,
                    )

                case_item.setExpanded(True)

            objective_item.setExpanded(True)

        if standalone_records:
            other_item = QTreeWidgetItem(
                ["Other Design Events"]
            )

            self.trace_tree.addTopLevelItem(
                other_item
            )

            for record in standalone_records:
                event_text = (
                    record.event_type.value
                )

                if record.recorded_at:
                    event_text += (
                        " — "
                        f"{self._format_timestamp(record.recorded_at)}"
                    )

                event_item = QTreeWidgetItem(
                    other_item,
                    [event_text],
                )

                event_item.setData(
                    0,
                    Qt.ItemDataRole.UserRole,
                    record,
                )

            other_item.setExpanded(True)

        self.detail_label.setText(
            "Select a design event to review "
            "how the decision was developed, "
            "reviewed and resolved."
        )
    @staticmethod
    def _proposal_outcome(records):
        event_names = [
            record.event_type.value
            for record in records
        ]

        if "Applied to Design" in event_names:
            return "Applied"

        if "Proposal Rejected" in event_names:
            return "Rejected"

        if "Proposal Accepted" in event_names:
            return "Accepted — Not Applied"

        if "Review Started" in event_names:
            return "In Review"

        return "Proposed — Not Yet Reviewed"

    def _proposal_timestamp(
        self,
        records,
    ):
        if not records:
            return ""

        latest_record = records[-1]

        if not latest_record.recorded_at:
            return ""

        return self._format_timestamp(
            latest_record.recorded_at
        )
    def _trace_selected(
        self,
        current,
        previous,
    ):
        if current is None:
            self.detail_label.setText(
                "Select a trace record to review "
                "its design provenance."
            )
            return

        record = current.data(
            0,
            Qt.ItemDataRole.UserRole,
        )

        if record is None:
            self.detail_label.setText(
                "Select an event within this "
                "proposal lifecycle to review "
                "its design provenance."
            )
            return

        proposed_text = self._format_content(
            record.proposed_content,
            "No Exercise Director proposal recorded.",
        )

        reviewed_text = self._format_content(
            record.reviewed_content,
            "No designer-reviewed content recorded.",
        )

        resulting_text = self._format_content(
            record.resulting_content,
            "No authoritative design change recorded.",
        )

        sources_text = self._format_content(
            record.source_references,
            "No source references recorded.",
        )

        rationale = (
            record.rationale.strip()
            or "No decision rationale recorded."
        )

        proposal_id = (
            record.proposal_id.strip()
            or "No proposal ID recorded."
        )

        recorded_by = (
            record.recorded_by.strip()
            or "Not recorded."
        )

        recorded_at = (
            self._format_timestamp(
                record.recorded_at
            )
            if record.recorded_at
            else "Not recorded."
        )

        detail = (
            f"EVENT\n"
            f"{record.event_type.value}\n\n"

            f"OBJECTIVE\n"
            f"{record.objective_title}\n\n"

            f"RECORDED BY\n"
            f"{recorded_by}\n\n"

            f"RECORDED AT\n"
            f"{recorded_at}\n\n"

            f"PROPOSAL ID\n"
            f"{proposal_id}\n\n"

            f"EXERCISE DIRECTOR PROPOSED\n"
            f"{proposed_text}\n\n"

            f"DESIGNER REVIEWED\n"
            f"{reviewed_text}\n\n"

            f"RESULTING AUTHORITATIVE DESIGN\n"
            f"{resulting_text}\n\n"

            f"DECISION RATIONALE\n"
            f"{rationale}\n\n"

            f"SOURCES\n"
            f"{sources_text}"
        )

        self.detail_label.setText(
            detail
        )
    @staticmethod
    def _format_timestamp(value):
        if not value:
            return ""

        try:
            timestamp = datetime.fromisoformat(
                value
            )

            return timestamp.strftime(
                "%d %b %Y  %H:%M:%S"
            )

        except ValueError:
            return value