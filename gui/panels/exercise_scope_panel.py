from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class ExerciseScopePanel(QWidget):
    """
    Workspace for defining the agreed scope of an
    exercise before detailed design begins.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.project = None

        layout = QVBoxLayout(self)

        heading = QLabel("SCOPE THE EXERCISE")
        heading.setStyleSheet(
            "font-size: 20px; "
            "font-weight: bold;"
        )

        introduction = QLabel(
            "Define what exercise is required, "
            "why it is required, and the boundaries "
            "within which it will be designed."
        )
        introduction.setWordWrap(True)

        self.project_label = QLabel(
            "No exercise project loaded."
        )
        self.project_label.setWordWrap(True)

        layout.addWidget(heading)
        layout.addWidget(introduction)
        layout.addWidget(self.project_label)

        commissioning_heading = QLabel(
            "COMMISSIONING BASIS"
        )
        commissioning_heading.setStyleSheet(
            "font-size: 14px; "
            "font-weight: bold; "
            "margin-top: 12px;"
        )
        layout.addWidget(commissioning_heading)

        commissioning_frame = QFrame()
        commissioning_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        commissioning_layout = QVBoxLayout(
            commissioning_frame
        )

        self.requirement_label = QLabel(
            "Requirement: Not recorded"
        )
        self.requirement_label.setWordWrap(True)

        self.sponsor_label = QLabel(
            "Sponsor: Not recorded"
        )
        self.sponsor_label.setWordWrap(True)

        self.operational_driver_label = QLabel(
            "Operational Driver: Not recorded"
        )
        self.operational_driver_label.setWordWrap(True)

        self.readiness_gap_label = QLabel(
            "Readiness Gap: Not recorded"
        )
        self.readiness_gap_label.setWordWrap(True)

        self.preparation_requirement_label = QLabel(
            "Preparation Requirement: Not recorded"
        )
        self.preparation_requirement_label.setWordWrap(
            True
        )

        commissioning_layout.addWidget(
            self.requirement_label
        )
        commissioning_layout.addWidget(
            self.sponsor_label
        )
        commissioning_layout.addWidget(
            self.operational_driver_label
        )
        commissioning_layout.addWidget(
            self.readiness_gap_label
        )
        commissioning_layout.addWidget(
            self.preparation_requirement_label
        )

        layout.addWidget(commissioning_frame)
        layout.addStretch()
    def set_project(self, project):
        self.project = project

        if project is None:
            self.project_label.setText(
                "No exercise project loaded."
            )
            self.requirement_label.setText(
                "Requirement: Not recorded"
            )
            self.sponsor_label.setText(
                "Sponsor: Not recorded"
            )
            self.operational_driver_label.setText(
                "Operational Driver: Not recorded"
            )
            self.readiness_gap_label.setText(
                "Readiness Gap: Not recorded"
            )
            self.preparation_requirement_label.setText(
                "Preparation Requirement: Not recorded"
            )
            return

        project_name = (
            getattr(project, "name", "")
            or "Untitled Project"
        )

        self.project_label.setText(
            f"Current Exercise: {project_name}"
        )
        requirement = project.operational_requirement
        readiness = requirement.readiness
        readiness_gap = readiness.readiness_gap
        if isinstance(readiness_gap, str):
            readiness_gap_shortfall = readiness_gap
            preparation_requirement = ""
        else:
            readiness_gap_shortfall = (
                readiness_gap.shortfall
            )
            preparation_requirement = (
                readiness_gap.preparation_requirement
    )

        self.requirement_label.setText(
            "Requirement: "
            f"{requirement.description or 'Not recorded'}"
        )

        self.sponsor_label.setText(
            "Sponsor: "
            f"{requirement.sponsor or 'Not recorded'}"
        )

        self.operational_driver_label.setText(
            "Operational Driver: "
            f"{requirement.operational_driver or 'Not recorded'}"
        )

        self.readiness_gap_label.setText(
            "Readiness Gap: "
            f"{readiness_gap_shortfall or 'Not recorded'}"
        )

        self.preparation_requirement_label.setText(
            "Preparation Requirement: "
            f"{preparation_requirement or 'Not recorded'}"
        )