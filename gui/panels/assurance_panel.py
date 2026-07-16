from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)


class AssurancePanel(QGroupBox):
    """
    Displays results produced by the Exercise Assurance Engine.

    This panel presents assurance information only.
    It does not perform assurance checks itself.
    """

    open_workspace_requested = Signal()

    def __init__(self):
        super().__init__("Exercise Assurance")

        layout = QVBoxLayout()

        self.project_name = QLabel("Untitled Project")

        project_font = QFont()
        project_font.setPointSize(12)
        project_font.setBold(True)

        self.project_name.setFont(project_font)
        layout.addWidget(self.project_name)

        layout.addWidget(QLabel("Overall Assessment"))

        self.status = QLabel("NOT CHECKED")

        status_font = QFont()
        status_font.setPointSize(18)
        status_font.setBold(True)

        self.status.setFont(status_font)
        layout.addWidget(self.status)

        layout.addWidget(QLabel("Evidence Summary"))

        self.summary = QLabel("No assurance results available.")
        self.summary.setWordWrap(True)
        layout.addWidget(self.summary)

        layout.addWidget(QLabel("Outstanding Actions"))

        self.findings = QListWidget()
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

        self.setLayout(layout)

    def show_results(self, results):
        self.findings.clear()

        self.project_name.setText(
            results.get("project_name", "Untitled Project")
        )

        inject_count = results.get("inject_count", 0)
        findings = results.get("findings", [])

        critical_count = sum(
            finding.severity == "Critical"
            for finding in findings
        )

        advisory_count = sum(
            finding.severity == "Advisory"
            for finding in findings
        )

        if critical_count > 0:
            self.status.setText("ACTION REQUIRED")
            self.recommendation.setText(
                "Resolve all critical findings before exercise delivery."
            )
            self.open_workspace_button.setText(
                "Open Workspace to Resolve Issues"
            )

        elif advisory_count > 0:
            self.status.setText("ASSURED WITH ADVISORIES")
            self.recommendation.setText(
                "The exercise is suitable for delivery, "
                "but the advisories should be reviewed."
            )
            self.open_workspace_button.setText(
                "Open Exercise Workspace"
            )

        else:
            self.status.setText("ASSURED")
            self.recommendation.setText(
                "No further action is required. "
                "The exercise is ready for delivery."
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
                "No outstanding assurance actions were identified."
            )

    def clear(self):
        self.project_name.setText("Untitled Project")
        self.status.setText("NOT CHECKED")
        self.summary.setText("No assurance results available.")
        self.findings.clear()
        self.recommendation.setText("")
        self.open_workspace_button.setText(
            "Open Exercise Workspace"
        )