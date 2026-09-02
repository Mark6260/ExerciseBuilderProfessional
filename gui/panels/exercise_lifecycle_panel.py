from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ExerciseLifecyclePanel(QWidget):
    commission_requested = Signal()
    scope_requested = Signal()
    """
    Exercise Director lifecycle overview.

    Presents the universal exercise and training process without
    assuming a particular sector, doctrine or exercise type.
    """

    def __init__(self):
        super().__init__()

        self.project = None

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        heading = QLabel("Exercise Director")
        heading.setStyleSheet(
            "font-size: 26px; font-weight: bold;"
        )
        main_layout.addWidget(heading)

        tagline = QLabel(
            "Better prepared today. Stronger tomorrow."
        )
        tagline.setStyleSheet(
            "font-size: 14px;"
        )
        main_layout.addWidget(tagline)

        golden_thread_heading = QLabel(
            "THE GOLDEN THREAD"
        )
        golden_thread_heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        main_layout.addWidget(golden_thread_heading)

        golden_thread_description = QLabel(
            "What are we preparing people or organisations "
            "to demonstrate, and how will we know?"
        )
        golden_thread_description.setWordWrap(True)
        main_layout.addWidget(
            golden_thread_description
        )

        self.golden_thread = QLabel(
            "REQUIREMENT  →  READINESS GAP  →  OBJECTIVES  →  "
            "CAPABILITY / SKILLS  →  EXERCISE OPPORTUNITIES  →  "
            "EVIDENCE  →  ASSESSMENT  →  "
            "IMPROVEMENT / READINESS"
        )
        self.golden_thread.setWordWrap(True)
        self.golden_thread.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.golden_thread.setStyleSheet(
            "font-size: 14px; "
            "font-weight: bold; "
            "padding: 18px;"
        )

        golden_thread_frame = QFrame()
        golden_thread_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        golden_thread_layout = QVBoxLayout(
            golden_thread_frame
        )
        golden_thread_layout.addWidget(
            self.golden_thread
        )

        main_layout.addWidget(
            golden_thread_frame
        )

        lifecycle_heading = QLabel(
            "EXERCISE LIFECYCLE"
        )
        lifecycle_heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        main_layout.addWidget(lifecycle_heading)

        lifecycle_description = QLabel(
            "Where are we in the professional exercise process?"
        )
        main_layout.addWidget(
            lifecycle_description
        )

        lifecycle_layout = QHBoxLayout()
        lifecycle_layout.setSpacing(8)

        self.lifecycle_labels = []

        stages = [
            "COMMISSION",
            "SCOPE",
            "DESIGN",
            "ASSURE",
            "DELIVER",
            "EVALUATE",
            "IMPROVE",
        ]

        for stage in stages:
            if stage == "COMMISSION":
                stage_widget = QPushButton(stage)
                stage_widget.clicked.connect(
                    self.commission_requested.emit
                )
            elif stage == "SCOPE":
                stage_widget = QPushButton(stage)
                stage_widget.clicked.connect(
                    self.scope_requested.emit
                )
            else:
                stage_widget = QLabel(stage)
                stage_widget.setAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

            stage_widget.setMinimumHeight(60)
            stage_widget.setStyleSheet(
                "font-weight: bold; "
                "padding: 10px; "
                "border: 1px solid palette(mid);"
            )

            lifecycle_layout.addWidget(
                stage_widget
            )
            self.lifecycle_labels.append(
                stage_widget
            )

        main_layout.addLayout(
            lifecycle_layout
        )
        current_exercise_heading = QLabel(
            "CURRENT EXERCISE"
        )
        current_exercise_heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        current_exercise_frame = QFrame()
        current_exercise_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        current_exercise_layout = QVBoxLayout(
            current_exercise_frame
        )
        current_exercise_layout.addWidget(
            current_exercise_heading
        )

        self.project_name_label = QLabel(
            "Exercise: No project loaded"
        )
        self.project_name_label.setStyleSheet(
            "font-size: 15px; font-weight: bold;"
        )
        current_exercise_layout.addWidget(
            self.project_name_label
        )

        requirement_heading = QLabel(
            "Requirement"
        )
        requirement_heading.setStyleSheet(
            "font-weight: bold;"
        )
        current_exercise_layout.addWidget(
            requirement_heading
        )

        self.requirement_label = QLabel(
            "No requirement recorded."
        )
        self.requirement_label.setWordWrap(True)
        self.requirement_label.setMinimumHeight(45)

        current_exercise_layout.addWidget(
            self.requirement_label
        )
        self.participants_label = QLabel(
            "Participants: Not recorded"
        )
        self.participants_label.setWordWrap(True)
        current_exercise_layout.addWidget(
            self.participants_label
        )
        self.sponsor_label = QLabel(
            "Sponsor: Not recorded"
        )
        self.sponsor_label.setWordWrap(True)
        current_exercise_layout.addWidget(
            self.sponsor_label
        )

        self.driver_label = QLabel(
            "Operational Driver: Not recorded"
        )
        self.driver_label.setWordWrap(True)
        current_exercise_layout.addWidget(
            self.driver_label
        )

        dashboard_layout = QHBoxLayout()
        dashboard_layout.setSpacing(16)

        dashboard_layout.addWidget(
            current_exercise_frame,
            1,
        )
        readiness_heading = QLabel(
            "READINESS POSITION"
        )
        readiness_heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        readiness_layout_heading = (
            readiness_heading
        )

        readiness_frame = QFrame()
        readiness_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        readiness_layout = QVBoxLayout(
            readiness_frame
        )

        self.current_state_label = QLabel(
            "Current State: Not recorded"
        )
        self.current_state_label.setWordWrap(True)
        readiness_layout.addWidget(
            self.current_state_label
        )

        self.required_state_label = QLabel(
            "Required State: Not recorded"
        )
        self.required_state_label.setWordWrap(True)
        readiness_layout.addWidget(
            self.required_state_label
        )

        self.required_standard_label = QLabel(
            "Required Standard: Not recorded"
        )
        self.required_standard_label.setWordWrap(True)
        readiness_layout.addWidget(
            self.required_standard_label
        )

        self.shortfall_label = QLabel(
            "Identified Shortfall: Not recorded"
        )
        self.shortfall_label.setWordWrap(True)
        readiness_layout.addWidget(
            self.shortfall_label
        )

        self.preparation_label = QLabel(
            "Preparation Requirement: Not recorded"
        )
        self.preparation_label.setWordWrap(True)
        readiness_layout.addWidget(
            self.preparation_label
        )

        readiness_layout.insertWidget(
            0,
            readiness_layout_heading,
        )

        dashboard_layout.addWidget(
            readiness_frame,
            1,
        )

        main_layout.addLayout(
            dashboard_layout
        )
        demonstrated_heading = QLabel(
            "WHAT MUST BE DEMONSTRATED?"
        )
        demonstrated_heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        main_layout.addWidget(
            demonstrated_heading
        )

        demonstrated_frame = QFrame()
        demonstrated_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        demonstrated_layout = QVBoxLayout(
            demonstrated_frame
        )

        self.objectives_summary_label = QLabel(
            "No exercise objectives recorded."
        )
        self.objectives_summary_label.setWordWrap(True)

        demonstrated_layout.addWidget(
            self.objectives_summary_label
        )

        main_layout.addWidget(
            demonstrated_frame
        )
        

        main_layout.addStretch(1)

        principle = QLabel(
            "Sector agnostic  •  Exercise-type agnostic  •  "
            "Doctrine adaptable  •  Professional process constant"
        )
        principle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        principle.setWordWrap(True)
        principle.setStyleSheet(
            "font-size: 13px; font-weight: bold;"
        )

        main_layout.addWidget(principle)

    def set_project(self, project):
        """
        Display the current project's core requirement.
        """

        self.project = project

        if project is None:
            self.project_name_label.setText(
                "Exercise: No project loaded"
            )
            self.requirement_label.setText(
                "No requirement recorded."
            )
            self.participants_label.setText(
                "Participants: Not recorded"
            )
            self.sponsor_label.setText(
                "Sponsor: Not recorded"
            )
            self.driver_label.setText(
                "Operational Driver: Not recorded"
            )
            self.current_state_label.setText(
                "Current State: Not recorded"
            )
            self.required_state_label.setText(
                "Required State: Not recorded"
            )
            self.required_standard_label.setText(
                "Required Standard: Not recorded"
            )
            self.shortfall_label.setText(
                "Identified Shortfall: Not recorded"
            )
            self.preparation_label.setText(
                "Preparation Requirement: Not recorded"
            )
            self.objectives_summary_label.setText(
                "No exercise objectives recorded."
            )
            return

        project_name = (
            getattr(project, "name", "") or ""
        ).strip()

        operational_requirement = getattr(
            project,
            "operational_requirement",
            None,
        )

        requirement = ""
        participants = ""
        sponsor = ""
        operational_driver = ""
        current_state = ""
        required_state = ""
        required_standard = ""
        shortfall = ""
        preparation_requirement = ""

        if operational_requirement is not None:
            requirement = (
                getattr(
                    operational_requirement,
                    "description",
                    "",
                )
                or ""
            ).strip()

            sponsor = (
                getattr(
                    operational_requirement,
                    "sponsor",
                    "",
                )
                or ""
            ).strip()

            operational_driver = (
                getattr(
                    operational_requirement,
                    "operational_driver",
                    "",
                )
                or ""
            ).strip()
            readiness = getattr(
                operational_requirement,
                "readiness",
                None,
            )
            participants = (
                getattr(
                    project,
                    "participants",
                    "",
                )
                or ""
            ).strip()
            if readiness is not None:
                current_state = (
                    getattr(
                        readiness,
                        "current_state",
                        "",
                    )
                    or ""
                ).strip()
                objectives = getattr(
                    project,
                    "objectives",
                    [],
                ) or []

                required_state = (
                    getattr(
                        readiness,
                        "required_state",
                        "",
                    )
                    or ""
                ).strip()

                required_standard = (
                    getattr(
                        readiness,
                        "required_standard",
                        "",
                    )
                    or ""
                ).strip()

                readiness_gap = getattr(
                    readiness,
                    "readiness_gap",
                    None,
                )

                if readiness_gap is not None:
                    shortfall = (
                        getattr(
                            readiness_gap,
                            "shortfall",
                            "",
                        )
                        or ""
                    ).strip()

                    preparation_requirement = (
                        getattr(
                            readiness_gap,
                            "preparation_requirement",
                            "",
                        )
                        or ""
                    ).strip()
        if objectives:
            objective_lines = []

            for index, objective in enumerate(
                objectives,
                start=1,
            ):
                title = (
                    getattr(
                        objective,
                        "title",
                        "",
                    )
                    or ""
                ).strip()

                description = (
                    getattr(
                        objective,
                        "description",
                        "",
                    )
                    or ""
                ).strip()

                if not title:
                    title = (
                        f"Objective {index}"
                    )

                objective_text = (
                    f"{index}. {title}"
                )

                if description:
                    objective_text += (
                        f"\n   {description}"
                    )

                objective_lines.append(
                    objective_text
                )

            self.objectives_summary_label.setText(
                "\n\n".join(
                    objective_lines
                )
            )
        else:
            self.objectives_summary_label.setText(
                "No exercise objectives recorded."
            )

        if project_name:
            self.project_name_label.setText(
                f"Exercise: {project_name}"
            )
        else:
            self.project_name_label.setText(
                "Exercise: Untitled Exercise"
            )

        if requirement:
            self.requirement_label.setText(
                requirement
            )
        else:
            self.requirement_label.setText(
                "No requirement recorded."
            )
        if participants:
            self.participants_label.setText(
                f"Participants: {participants}"
            )
        else:
            self.participants_label.setText(
                "Participants: Not recorded"
            )
        if sponsor:
            self.sponsor_label.setText(
                f"Sponsor: {sponsor}"
            )
        else:
            self.sponsor_label.setText(
                "Sponsor: Not recorded"
            )

        if operational_driver:
            self.driver_label.setText(
                "Operational Driver: "
                f"{operational_driver}"
            )
        else:
            self.driver_label.setText(
                "Operational Driver: Not recorded"
            )
            self.current_state_label.setText(
            "Current State: "
            f"{current_state or 'Not recorded'}"
        )

        self.required_state_label.setText(
            "Required State: "
            f"{required_state or 'Not recorded'}"
        )

        self.required_standard_label.setText(
            "Required Standard: "
            f"{required_standard or 'Not recorded'}"
        )

        self.shortfall_label.setText(
            "Identified Shortfall: "
            f"{shortfall or 'Not recorded'}"
        )

        self.preparation_label.setText(
            "Preparation Requirement: "
            f"{preparation_requirement or 'Not recorded'}"
        )