from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class AssurancePanel(QGroupBox):
    """
    Displays results produced by the Exercise Assurance Engine.

    Design assurance and performance/readiness assurance are presented
    separately. This panel reports recorded readiness decisions; it does
    not make or infer readiness decisions itself.
    """

    open_workspace_requested = Signal()

    def __init__(self):
        super().__init__("Exercise Assurance")

        content = QWidget()
        layout = QVBoxLayout(content)

        self.project_name = QLabel("Untitled Project")

        project_font = QFont()
        project_font.setPointSize(12)
        project_font.setBold(True)

        self.project_name.setFont(project_font)
        layout.addWidget(self.project_name)

        layout.addWidget(
            self._section_heading("DESIGN ASSURANCE")
        )

        layout.addWidget(QLabel("Overall Assessment"))

        self.status = QLabel("NOT CHECKED")

        status_font = QFont()
        status_font.setPointSize(18)
        status_font.setBold(True)

        self.status.setFont(status_font)
        layout.addWidget(self.status)

        layout.addWidget(QLabel("Design Assurance Summary"))

        self.summary = QLabel("No assurance results available.")
        self.summary.setWordWrap(True)
        layout.addWidget(self.summary)

        layout.addWidget(QLabel("Outstanding Actions"))

        self.findings = QListWidget()
        self.findings.setMinimumHeight(180)
        layout.addWidget(self.findings)

        layout.addWidget(QLabel("Recommendation"))

        self.recommendation = QLabel("")
        self.recommendation.setWordWrap(True)
        layout.addWidget(self.recommendation)

        self.open_workspace_button = QPushButton(
            "Open Exercise Workspace"
        )
        self.open_workspace_button.clicked.connect(
            self.open_workspace_requested.emit
        )

        layout.addWidget(self.open_workspace_button)

        layout.addWidget(
            self._section_heading(
                "PERFORMANCE & READINESS ASSURANCE"
            )
        )

        performance_note = QLabel(
            "This section reports the evidence, assessment and "
            "authorised readiness-decision trail recorded in "
            "Exercise Director. It does not determine readiness."
        )
        performance_note.setWordWrap(True)
        performance_note.setStyleSheet(
            "font-style: italic;"
        )
        layout.addWidget(performance_note)

        self.performance_summary = QLabel(
            "No performance assurance results available."
        )
        self.performance_summary.setWordWrap(True)
        self.performance_summary.setTextInteractionFlags(
            self.performance_summary.textInteractionFlags()
        )
        layout.addWidget(self.performance_summary)

        layout.addWidget(
            self._section_heading(
                "LATEST AUTHORISED READINESS DECISION"
            )
        )

        self.readiness_status = QLabel(
            "NO AUTHORISED DECISION RECORDED"
        )

        readiness_font = QFont()
        readiness_font.setPointSize(16)
        readiness_font.setBold(True)

        self.readiness_status.setFont(
            readiness_font
        )
        self.readiness_status.setWordWrap(True)
        layout.addWidget(self.readiness_status)

        self.readiness_detail = QLabel(
            "No readiness decision has been recorded."
        )
        self.readiness_detail.setWordWrap(True)
        layout.addWidget(self.readiness_detail)

        self.limitations_heading = QLabel(
            "Limitations"
        )
        self.limitations_heading.setStyleSheet(
            "font-weight: bold;"
        )
        self.limitations_heading.setVisible(False)
        layout.addWidget(self.limitations_heading)

        self.limitations = QLabel("")
        self.limitations.setWordWrap(True)
        self.limitations.setVisible(False)
        layout.addWidget(self.limitations)

        self.required_action_heading = QLabel(
            "Required Action"
        )
        self.required_action_heading.setStyleSheet(
            "font-weight: bold;"
        )
        self.required_action_heading.setVisible(False)
        layout.addWidget(
            self.required_action_heading
        )

        self.required_action = QLabel("")
        self.required_action.setWordWrap(True)
        self.required_action.setVisible(False)
        layout.addWidget(self.required_action)

        layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content)

        wrapper = QVBoxLayout()
        wrapper.addWidget(scroll)

        self.setLayout(wrapper)

    @staticmethod
    def _section_heading(text):
        label = QLabel(text)

        font = QFont()
        font.setPointSize(12)
        font.setBold(True)

        label.setFont(font)
        return label

    def show_results(self, results):
        self.findings.clear()

        self.project_name.setText(
            results.get(
                "project_name",
                "Untitled Project",
            )
        )

        inject_count = results.get(
            "inject_count",
            0,
        )
        findings = results.get(
            "findings",
            [],
        )

        critical_count = sum(
            finding.severity == "Critical"
            for finding in findings
        )

        advisory_count = sum(
            finding.severity == "Advisory"
            for finding in findings
        )

        if critical_count > 0:
            self.status.setText(
                "ACTION REQUIRED"
            )
            self.recommendation.setText(
                "Resolve all critical findings before exercise delivery."
            )
            self.open_workspace_button.setText(
                "Open Workspace to Resolve Issues"
            )

        elif advisory_count > 0:
            self.status.setText(
                "ASSURED WITH ADVISORIES"
            )
            self.recommendation.setText(
                "The exercise is suitable for delivery, "
                "but the advisories should be reviewed."
            )
            self.open_workspace_button.setText(
                "Open Exercise Workspace"
            )

        else:
            self.status.setText(
                "ASSURED"
            )
            self.recommendation.setText(
                "No further design-assurance action is required "
                "before exercise delivery."
            )
            self.open_workspace_button.setText(
                "Proceed to Exercise Workspace"
            )

        self.summary.setText(
            f"{inject_count} injects checked\n"
            f"{critical_count} critical findings\n"
            f"{advisory_count} advisories"
        )

        if findings:
            for finding in findings:
                item = QListWidgetItem(
                    f"{finding.severity}: {finding.item}\n"
                    f"{finding.message}\n"
                    f"Recommended action: "
                    f"{finding.recommendation}"
                )

                item.setToolTip(
                    f"Category: {finding.category}"
                )

                self.findings.addItem(item)

        else:
            self.findings.addItem(
                "No outstanding design-assurance actions "
                "were identified."
            )

        self._show_performance_assurance(
            results.get(
                "performance_assurance",
                {},
            )
        )

    def _show_performance_assurance(
        self,
        performance,
    ):
        observation_count = performance.get(
            "observation_count",
            0,
        )
        reviewed_count = performance.get(
            "reviewed_observation_count",
            0,
        )
        evidence_count = performance.get(
            "evidence_count",
            0,
        )
        assessment_count = performance.get(
            "assessment_count",
            0,
        )
        decision_count = performance.get(
            "readiness_decision_count",
            0,
        )

        self.performance_summary.setText(
            f"Observations: {observation_count} recorded / "
            f"{reviewed_count} reviewed\n"
            f"Evidence records admitted: {evidence_count}\n"
            f"Professional assessments recorded: "
            f"{assessment_count}\n"
            f"Authorised readiness decisions recorded: "
            f"{decision_count}"
        )

        outcome = performance.get(
            "readiness_outcome",
            "",
        )

        if not outcome:
            self.readiness_status.setText(
                "NO AUTHORISED DECISION RECORDED"
            )
            self.readiness_detail.setText(
                "No readiness decision has been recorded."
            )
            self._show_optional_decision_fields(
                "",
                "",
            )
            return

        self.readiness_status.setText(
            outcome.upper()
        )

        decision_maker = performance.get(
            "decision_maker",
            "",
        )
        decision_authority = performance.get(
            "decision_authority",
            "",
        )
        recorded_at = performance.get(
            "recorded_at",
            "",
        )

        detail_lines = []

        if decision_maker:
            detail_lines.append(
                f"Decision-maker: {decision_maker}"
            )

        if decision_authority:
            detail_lines.append(
                f"Authority: {decision_authority}"
            )

        if recorded_at:
            detail_lines.append(
                f"Recorded: {recorded_at}"
            )

        if not detail_lines:
            detail_lines.append(
                "An authorised readiness decision has "
                "been recorded."
            )

        self.readiness_detail.setText(
            "\n".join(detail_lines)
        )

        self._show_optional_decision_fields(
            performance.get(
                "limitations",
                "",
            ),
            performance.get(
                "required_action",
                "",
            ),
        )

    def _show_optional_decision_fields(
        self,
        limitations,
        required_action,
    ):
        has_limitations = bool(
            limitations.strip()
        )
        has_required_action = bool(
            required_action.strip()
        )

        self.limitations_heading.setVisible(
            has_limitations
        )
        self.limitations.setVisible(
            has_limitations
        )
        self.limitations.setText(
            limitations
        )

        self.required_action_heading.setVisible(
            has_required_action
        )
        self.required_action.setVisible(
            has_required_action
        )
        self.required_action.setText(
            required_action
        )

    def clear(self):
        self.project_name.setText(
            "Untitled Project"
        )
        self.status.setText(
            "NOT CHECKED"
        )
        self.summary.setText(
            "No assurance results available."
        )
        self.findings.clear()
        self.recommendation.setText("")
        self.open_workspace_button.setText(
            "Open Exercise Workspace"
        )

        self.performance_summary.setText(
            "No performance assurance results available."
        )
        self.readiness_status.setText(
            "NO AUTHORISED DECISION RECORDED"
        )
        self.readiness_detail.setText(
            "No readiness decision has been recorded."
        )
        self._show_optional_decision_fields(
            "",
            "",
        )