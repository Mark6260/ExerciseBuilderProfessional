from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ExerciseDesignPanel(QWidget):
    """
    Derived exercise-design view built from the assured CTO.

    This panel does not create or alter the CTO. It translates the
    Project-owned CTO into exercise design requirements so the designer
    can see what the exercise must create opportunities to demonstrate
    and what evidence the exercise must be capable of producing.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.project = None
        self.cto = None

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )
        layout.setSpacing(12)

        title = QLabel(
            "EXERCISE DESIGN FROM ASSURED CTO"
        )
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )
        layout.addWidget(title)

        guidance = QLabel(
            "Translate the assured Collective Training Objective into "
            "requirements for exercise design. Exercise Director shows "
            "what the exercise must create an opportunity to demonstrate "
            "and what evidence it must be capable of producing."
        )
        guidance.setWordWrap(True)
        layout.addWidget(guidance)

        status_frame = QFrame()
        status_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )
        status_layout = QVBoxLayout(
            status_frame
        )

        self.status_label = QLabel(
            "No project loaded"
        )
        self.status_label.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        self.status_label.setWordWrap(True)

        self.status_detail = QLabel("")
        self.status_detail.setWordWrap(True)

        status_layout.addWidget(
            self.status_label
        )
        status_layout.addWidget(
            self.status_detail
        )

        layout.addWidget(
            status_frame
        )

        self.design_tree = QTreeWidget()
        self.design_tree.setColumnCount(3)
        self.design_tree.setHeaderLabels(
            [
                "Design Level",
                "Assured Requirement",
                "Exercise Design Implication",
            ]
        )
        self.design_tree.setAlternatingRowColors(
            True
        )
        self.design_tree.setRootIsDecorated(
            True
        )
        self.design_tree.setUniformRowHeights(
            False
        )

        self.design_tree.header().setStretchLastSection(
            True
        )

        self.design_tree.setColumnWidth(
            0,
            190,
        )
        self.design_tree.setColumnWidth(
            1,
            430,
        )

        layout.addWidget(
            self.design_tree,
            1,
        )

        footer_layout = QHBoxLayout()

        self.refresh_button = QPushButton(
            "REFRESH FROM CTO"
        )
        self.refresh_button.clicked.connect(
            self.refresh_view
        )

        footer_layout.addStretch()
        footer_layout.addWidget(
            self.refresh_button
        )

        layout.addLayout(
            footer_layout
        )

    def set_project(
        self,
        project,
    ):
        self.project = project
        self.refresh_view()

    def refresh_view(self):
        self.design_tree.clear()
        self.cto = None

        if self.project is None:
            self.status_label.setText(
                "NO PROJECT LOADED"
            )
            self.status_detail.setText(
                "Open or create an Exercise Director project."
            )
            return

        if not self.project.collective_training_objectives:
            self.status_label.setText(
                "NO CTO AVAILABLE"
            )
            self.status_detail.setText(
                "Complete the CTO Builder before exercise design begins."
            )
            return

        self.cto = (
            self.project.collective_training_objectives[0]
        )

        structure_ready = (
            self.cto.passes_collective_structure_test()
        )
        success_ready = (
            self.cto.has_evidence_coverage()
        )
        critical_ready = (
            self.cto.has_critical_error_coverage()
        )

        ready = (
            structure_ready
            and success_ready
            and critical_ready
        )

        if not ready:
            self.status_label.setText(
                "CTO NEEDS DEVELOPMENT"
            )
            self.status_detail.setText(
                "Exercise design is not yet released from the CTO "
                "assurance gate. Resolve the gaps identified in the "
                "CTO Design Review first."
            )
            self._show_blocking_gaps()
            return

        self.status_label.setText(
            "READY FOR EXERCISE DESIGN"
        )
        self.status_detail.setText(
            "The CTO has passed the current structural and evidence "
            "coverage checks. The requirements below are derived from "
            "that assured design basis. Professional judgement remains "
            "with the Exercise Director."
        )

        self._build_design_requirements()
        self.design_tree.expandAll()

    def _show_blocking_gaps(self):
        root = QTreeWidgetItem(
            [
                "Assurance Gate",
                "CTO is not ready for exercise design",
                "Return to CTO Builder → Design Review",
            ]
        )
        self.design_tree.addTopLevelItem(
            root
        )

        for reason in self.cto.collective_test_reasons():
            QTreeWidgetItem(
                root,
                [
                    "Structure Gap",
                    reason,
                    "Resolve before exercise design.",
                ],
            )

        for task in self.cto.collective_tasks:
            for factor in task.success_factors:
                if not factor.metrics:
                    item = QTreeWidgetItem(
                        root,
                        [
                            "Evidence Gap",
                            factor.description,
                            (
                                "Define at least one observable metric "
                                f"for task: {task.title}."
                            ),
                        ],
                    )
                    item.setData(
                        0,
                        Qt.ItemDataRole.UserRole,
                        factor.id,
                    )
                    continue

                for metric in factor.metrics:
                    if not metric.evidence_requirements:
                        item = QTreeWidgetItem(
                            root,
                            [
                                "Evidence Gap",
                                metric.description,
                                (
                                    "Define the evidence the exercise "
                                    "must be capable of producing."
                                ),
                            ],
                        )
                        item.setData(
                            0,
                            Qt.ItemDataRole.UserRole,
                            metric.id,
                        )

        for task in self.cto.collective_tasks:
            for error in task.critical_errors:
                if not error.metrics:
                    item = QTreeWidgetItem(
                        root,
                        [
                            "Critical Error Gap",
                            error.description,
                            (
                                "Define how this critical failure would "
                                "be observed."
                            ),
                        ],
                    )
                    item.setData(
                        0,
                        Qt.ItemDataRole.UserRole,
                        error.id,
                    )
                    continue

                for metric in error.metrics:
                    if not metric.evidence_requirements:
                        item = QTreeWidgetItem(
                            root,
                            [
                                "Critical Error Gap",
                                metric.description,
                                (
                                    "Define evidence for this critical "
                                    "error metric."
                                ),
                            ],
                        )
                        item.setData(
                            0,
                            Qt.ItemDataRole.UserRole,
                            metric.id,
                        )

        self.design_tree.expandAll()

    def _build_design_requirements(self):
        cto_item = QTreeWidgetItem(
            [
                "Collective Outcome",
                self.cto.required_outcome,
                (
                    "The exercise must create a credible opportunity "
                    "for the training audience to demonstrate this "
                    "collective outcome."
                ),
            ]
        )
        cto_item.setData(
            0,
            Qt.ItemDataRole.UserRole,
            self.cto.id,
        )

        self.design_tree.addTopLevelItem(
            cto_item
        )

        for task in self.cto.collective_tasks:
            task_item = QTreeWidgetItem(
                cto_item,
                [
                    "Collective Task",
                    task.title,
                    (
                        "Create one or more exercise activities or "
                        "situations that require the collective to "
                        "perform this task."
                    ),
                ],
            )
            task_item.setData(
                0,
                Qt.ItemDataRole.UserRole,
                task.id,
            )

            for factor in task.success_factors:
                factor_item = QTreeWidgetItem(
                    task_item,
                    [
                        "Success Factor",
                        factor.description,
                        (
                            "Design the situation so successful "
                            "collective performance can be demonstrated."
                        ),
                    ],
                )
                factor_item.setData(
                    0,
                    Qt.ItemDataRole.UserRole,
                    factor.id,
                )

                for metric in factor.metrics:
                    metric_item = QTreeWidgetItem(
                        factor_item,
                        [
                            "Observable Metric",
                            metric.description,
                            (
                                "Ensure observers can see, hear, record "
                                "or measure this during exercise play."
                            ),
                        ],
                    )
                    metric_item.setData(
                        0,
                        Qt.ItemDataRole.UserRole,
                        metric.id,
                    )

                    for requirement in metric.evidence_requirements:
                        evidence_item = QTreeWidgetItem(
                            metric_item,
                            [
                                "Evidence Requirement",
                                requirement.description,
                                (
                                    "Exercise design must enable this "
                                    "evidence to be produced or captured"
                                    + (
                                        f" ({requirement.evidence_type})."
                                        if requirement.evidence_type
                                        else "."
                                    )
                                ),
                            ],
                        )
                        evidence_item.setData(
                            0,
                            Qt.ItemDataRole.UserRole,
                            requirement.id,
                        )

            for error in task.critical_errors:
                error_item = QTreeWidgetItem(
                    task_item,
                    [
                        "Critical Error",
                        error.description,
                        (
                            "Where appropriate, design conditions that "
                            "allow this serious failure to be recognised "
                            "without artificially forcing it to occur."
                        ),
                    ],
                )
                error_item.setData(
                    0,
                    Qt.ItemDataRole.UserRole,
                    error.id,
                )

                for metric in error.metrics:
                    metric_item = QTreeWidgetItem(
                        error_item,
                        [
                            "Critical Error Metric",
                            metric.description,
                            (
                                "Ensure observers can recognise this "
                                "failure if it occurs."
                            ),
                        ],
                    )
                    metric_item.setData(
                        0,
                        Qt.ItemDataRole.UserRole,
                        metric.id,
                    )

                    for requirement in metric.evidence_requirements:
                        evidence_item = QTreeWidgetItem(
                            metric_item,
                            [
                                "Evidence Requirement",
                                requirement.description,
                                (
                                    "Ensure this evidence can be captured "
                                    "if the critical error occurs"
                                    + (
                                        f" ({requirement.evidence_type})."
                                        if requirement.evidence_type
                                        else "."
                                    )
                                ),
                            ],
                        )
                        evidence_item.setData(
                            0,
                            Qt.ItemDataRole.UserRole,
                            requirement.id,
                        )
