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

        self.status = QLabel("NOT CHECKED")

        status_font = QFont()
        status_font.setPointSize(18)
        status_font.setBold(True)

        self.status.setFont(status_font)
        layout.addWidget(self.status)

        self.summary = QLabel("No assurance results available.")
        self.summary.setWordWrap(True)
        layout.addWidget(self.summary)

        self.findings = QListWidget()
        layout.addWidget(self.findings)

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
        elif advisory_count > 0:
            self.status.setText("ASSURED WITH ADVISORIES")
        else:
            self.status.setText("ASSURED")

        self.summary.setText(
            f"{inject_count} injects checked\n"
            f"{critical_count} critical findings\n"
            f"{advisory_count} advisories"
        )

        if not findings:
            self.findings.addItem(
                "No assurance findings were identified."
            )
            return

        for finding in findings:
            item = QListWidgetItem(
                f"{finding.severity}: {finding.item}\n"
                f"{finding.message}\n"
                f"Recommended action: {finding.recommendation}"
            )

            item.setToolTip(
                f"Category: {finding.category}"
            )

            self.findings.addItem(item)

    def clear(self):
        self.status.setText("NOT CHECKED")
        self.summary.setText("No assurance results available.")
        self.findings.clear()