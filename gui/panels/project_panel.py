from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLabel,
    QVBoxLayout,
)


class ProjectPanel(QGroupBox):
    def __init__(self):
        super().__init__("Operational Readiness")
        
        self.setMinimumWidth(360)

        self.name_label = QLabel("-")
        self.file_label = QLabel("-")

        self.target_readiness_label = QLabel("-")
        self.current_readiness_label = QLabel("-")
        self.required_standard_label = QLabel("-")
        self.readiness_gap_label = QLabel("-")
        self.operational_requirement_label = QLabel("-")

        labels = [
            self.name_label,
            self.file_label,
            self.target_readiness_label,
            self.current_readiness_label,
            self.required_standard_label,
            self.readiness_gap_label,
            self.operational_requirement_label,
        ]

        for label in labels:
            label.setWordWrap(True)

        identity_layout = QFormLayout()
        identity_layout.addRow(
            "Case:",
            self.name_label,
        )
        identity_layout.addRow(
            "File:",
            self.file_label,
        )

        readiness_layout = QFormLayout()
        readiness_layout.addRow(
            "Target Readiness:",
            self.target_readiness_label,
        )
        readiness_layout.addRow(
            "Current Readiness:",
            self.current_readiness_label,
        )
        readiness_layout.addRow(
            "Required Standard:",
            self.required_standard_label,
        )
        readiness_layout.addRow(
            "Readiness Gap:",
            self.readiness_gap_label,
        )
        readiness_layout.addRow(
            "Operational Requirement:",
            self.operational_requirement_label,
        )

        layout = QVBoxLayout()
        layout.addLayout(identity_layout)
        layout.addSpacing(10)
        layout.addLayout(readiness_layout)

        self.setLayout(layout)

    def update_project(
        self,
        name: str,
        filename: str | None = None,
        target_readiness: str = "",
        current_readiness: str = "",
        required_standard: str = "",
        readiness_gap: str = "",
        operational_requirement: str = "",
    ):
        self.name_label.setText(
            name or "Untitled Project"
        )

        self.file_label.setText(
            filename or "-"
        )

        self.target_readiness_label.setText(
            target_readiness or "Not yet defined"
        )

        self.current_readiness_label.setText(
            current_readiness or "Not yet defined"
        )

        self.required_standard_label.setText(
            required_standard or "Not yet defined"
        )

        self.readiness_gap_label.setText(
            readiness_gap or "Not yet defined"
        )

        self.operational_requirement_label.setText(
            operational_requirement or "Not yet defined"
        )