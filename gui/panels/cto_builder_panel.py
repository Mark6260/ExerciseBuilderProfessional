from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QSpinBox,
)

from core.collective_training_objective import (
    CollectiveTask,
    CollectiveTrainingObjective,
    CriticalError,
    EvidenceRequirement,
    PerformanceMetric,
    SuccessFactor,
)


class CTOBuilderPanel(QWidget):
    """
    Guided Collective Training Objective builder.

    The builder progressively constructs a real
    CollectiveTrainingObjective and provides design feedback
    from the domain model.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.cto = CollectiveTrainingObjective(
            title="Untitled CTO"
        )

        self.current_collective_task = None

        # Build all widgets first
        self._build_ui()

        # Then connect signals
        self.training_audience_input.textChanged.connect(
            self._update_training_audience
        )
        
        self.collective_outcome_input.textChanged.connect(
            self._update_collective_outcome
        )
        
        self.conditions_input.textChanged.connect(
            self._update_conditions
        )
        
        self.challenge_level_input.valueChanged.connect(
            self._update_challenge_level
        )
        
        self.add_success_factor_button.clicked.connect(
            self._add_success_factor
        )
        
        self.add_collective_task_button.clicked.connect(
            self._add_collective_task
        )
        self.collective_task_input.textChanged.connect(
            self._update_add_collective_task_button
        )
        self.critical_error_input.textChanged.connect(
            self._update_add_critical_error_button
        )
        self.critical_error_task_selector.currentIndexChanged.connect(
            self._update_add_critical_error_button
        )
        self.critical_error_evidence_input.textChanged.connect(
            self._update_add_critical_error_button
        )
        self.add_critical_error_button.clicked.connect(
            self._add_critical_error
        )

        self.metric_task_selector.currentIndexChanged.connect(
            self._refresh_metric_success_factor_selector
        )
        self.metric_success_factor_selector.currentIndexChanged.connect(
            self._update_add_observable_metric_button
        )
        self.observable_metric_input.textChanged.connect(
            self._update_add_observable_metric_button
        )
        self.add_observable_metric_button.clicked.connect(
            self._add_observable_metric
        )

        self.evidence_task_selector.currentIndexChanged.connect(
            self._refresh_evidence_success_factor_selector
        )
        self.evidence_success_factor_selector.currentIndexChanged.connect(
            self._refresh_evidence_metric_selector
        )
        self.evidence_metric_selector.currentIndexChanged.connect(
            self._update_add_evidence_requirement_button
        )
        self.evidence_description_input.textChanged.connect(
            self._update_add_evidence_requirement_button
        )
        self.evidence_type_input.textChanged.connect(
            self._update_add_evidence_requirement_button
        )
        self.add_evidence_requirement_button.clicked.connect(
            self._add_evidence_requirement
        )
        
    def _build_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )
        main_layout.setSpacing(12)

        # -------------------------------------------------
        # Stage navigation
        # -------------------------------------------------

        nav_frame = QFrame()
        nav_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        nav_layout = QVBoxLayout(
            nav_frame
        )

        nav_title = QLabel(
            "CTO BUILDER"
        )
        nav_title.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        nav_layout.addWidget(
            nav_title
        )

        self.stage_list = QListWidget()

        stages = [
            "1. Training Audience",
            "2. Collective Outcome",
            "3. Conditions & Challenge",
            "4. Collective Tasks & Success",
            "5. Critical Errors",
            "6. Observable Metrics",
            "7. Evidence Requirements",
            "Design Review",
        ]

        self.stage_list.addItems(
            stages
        )

        nav_layout.addWidget(
            self.stage_list
        )

        main_layout.addWidget(
            nav_frame,
            1,
        )

        # -------------------------------------------------
        # Working area
        # -------------------------------------------------

        work_frame = QFrame()
        work_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        work_layout = QVBoxLayout(
            work_frame
        )

        self.page_title = QLabel(
            "Training Audience"
        )
        self.page_title.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.guidance_label = QLabel(
            "Identify the collective whose performance "
            "is being developed or assessed."
        )
        self.guidance_label.setWordWrap(
            True
        )

        work_layout.addWidget(
            self.page_title
        )

        work_layout.addWidget(
            self.guidance_label
        )

        self.page_stack = QStackedWidget()

        # -------------------------------------------------
        # Stage 1 - Training Audience
        # -------------------------------------------------

        audience_page = QWidget()
        audience_layout = QVBoxLayout(
            audience_page
        )

        self.training_audience_input = QLineEdit()
        self.training_audience_input.setPlaceholderText(
            "e.g. Battlegroup Headquarters"
        )

        audience_layout.addWidget(
            self.training_audience_input
        )

        audience_layout.addStretch()

        self.page_stack.addWidget(
            audience_page
        )

        # -------------------------------------------------
        # Stage 2 - Collective Outcome
        # -------------------------------------------------

        outcome_page = QWidget()
        outcome_layout = QVBoxLayout(
            outcome_page
        )

        self.collective_outcome_input = QTextEdit()
        self.collective_outcome_input.setPlaceholderText(
            "Describe what the collective must achieve "
            "together..."
        )

        outcome_layout.addWidget(
            self.collective_outcome_input
        )

        self.page_stack.addWidget(
            outcome_page
        )

        # -------------------------------------------------
        # Stage 3 - Conditions & Challenge
        # -------------------------------------------------

        conditions_page = QWidget()

        conditions_layout = QVBoxLayout(
            conditions_page
        )

        conditions_label = QLabel(
            "Under what conditions must this collective perform?"
        )
        conditions_label.setWordWrap(
            True
        )

        self.conditions_input = QTextEdit()
        self.conditions_input.setPlaceholderText(
            "e.g. degraded communications, incomplete information, "
            "time pressure, competing priorities..."
        )

        challenge_label = QLabel(
            "Challenge Level (optional)"
        )
        challenge_label.setStyleSheet(
            "font-weight: bold;"
        )

        challenge_guidance = QLabel(
            "Use only where the training methodology defines "
            "a challenge level. Leave at 0 when not applicable."
        )
        challenge_guidance.setWordWrap(
            True
        )

        self.challenge_level_input = QSpinBox()
        self.challenge_level_input.setRange(
            0,
            10,
        )
        self.challenge_level_input.setSpecialValueText(
            "Not specified"
        )

        conditions_layout.addWidget(
            conditions_label
        )

        conditions_layout.addWidget(
            self.conditions_input
        )

        conditions_layout.addWidget(
            challenge_label
        )

        conditions_layout.addWidget(
            challenge_guidance
        )

        conditions_layout.addWidget(
            self.challenge_level_input
        )

        self.page_stack.addWidget(
            conditions_page
        )

        # -------------------------------------------------
        # Stage 4 - Collective Tasks & Success
        # -------------------------------------------------

        tasks_page = QWidget()

        tasks_layout = QVBoxLayout(
            tasks_page
        )

        task_guidance = QLabel(
            "Identify something the collective must do together "
            "to achieve the required outcome."
        )
        task_guidance.setWordWrap(
            True
        )

        task_label = QLabel(
            "COLLECTIVE TASK"
        )
        task_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.collective_task_input = QLineEdit()
        self.collective_task_input.setPlaceholderText(
            "e.g. Synchronise Activity"
        )

        success_label = QLabel(
            "WHAT DOES SUCCESSFUL COLLECTIVE "
            "PERFORMANCE LOOK LIKE?"
        )
        success_label.setStyleSheet(
            "font-weight: bold;"
        )
        success_label.setWordWrap(
            True
        )

        self.success_factor_input = QTextEdit()
        self.success_factor_input.setPlaceholderText(
            "e.g. Activity is synchronised in time and space"
        )
        self.success_factor_input.setMaximumHeight(
            100
        )

        self.add_success_factor_button = QPushButton(
            "ADD SUCCESS FACTOR"
        )

        current_task_label = QLabel(
            "CURRENT COLLECTIVE TASK"
        )
        current_task_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.current_task_summary = QTextEdit()
        self.current_task_summary.setReadOnly(
            True
        )
        self.current_task_summary.setPlaceholderText(
            "No collective task has been added yet."
        )

        self.add_collective_task_button = QPushButton(
            "ADD COLLECTIVE TASK"
        )
        self.add_collective_task_button.setEnabled(
            False
        )
        cto_tasks_label = QLabel(
            "CTO TASKS"
        )
        cto_tasks_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.cto_tasks_summary = QTextEdit()
        self.cto_tasks_summary.setReadOnly(
            True
        )
        self.cto_tasks_summary.setPlaceholderText(
            "No collective tasks have been added yet."
        )

        tasks_layout.addWidget(
            task_guidance
        )
        tasks_layout.addWidget(
            task_label
        )
        tasks_layout.addWidget(
            self.collective_task_input
        )
        tasks_layout.addWidget(
            success_label
        )
        tasks_layout.addWidget(
            self.success_factor_input
        )
        tasks_layout.addWidget(
            self.add_success_factor_button
        )
        tasks_layout.addWidget(
            current_task_label
        )
        tasks_layout.addWidget(
            self.current_task_summary
        )
        tasks_layout.addWidget(
            self.add_collective_task_button
        )
        tasks_layout.addWidget(
            cto_tasks_label
        )

        tasks_layout.addWidget(
            self.cto_tasks_summary
        )
        self.page_stack.addWidget(
            tasks_page
        )

        critical_errors_page = QWidget()

        critical_errors_layout = QVBoxLayout(
            critical_errors_page
        )

        critical_errors_guidance = QLabel(
            "Identify collective failures serious enough to "
            "undermine successful performance or the required "
            "collective outcome."
        )
        critical_errors_guidance.setWordWrap(
            True
        )

        critical_error_label = QLabel(
            "CRITICAL ERROR"
        )
        critical_error_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.critical_error_input = QTextEdit()
        self.critical_error_input.setPlaceholderText(
            "e.g. Activity becomes dangerously unsynchronised"
        )
        self.critical_error_input.setMaximumHeight(
            100
        )

        critical_evidence_label = QLabel(
            "WHAT WOULD SHOW THAT THIS CRITICAL ERROR OCCURRED?"
        )
        critical_evidence_label.setStyleSheet(
            "font-weight: bold;"
        )
        critical_evidence_label.setWordWrap(
            True
        )
        critical_error_task_label = QLabel(
            "COLLECTIVE TASK"
        )

        critical_error_task_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.critical_error_task_selector = (
            QComboBox()
        )

        self.critical_error_task_selector.setPlaceholderText(
            "Select the collective task"
        )

        self.critical_error_evidence_input = QTextEdit()
        self.critical_error_evidence_input.setPlaceholderText(
            "e.g. Conflicting activity creates unacceptable "
            "operational risk"
        )
        self.critical_error_evidence_input.setMaximumHeight(
            100
        )

        self.add_critical_error_button = QPushButton(
            "ADD CRITICAL ERROR"
        )

        self.add_critical_error_button.setEnabled(
            False
        )

        critical_errors_summary_label = QLabel(
            "CTO CRITICAL ERRORS"
        )
        critical_errors_summary_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.critical_errors_summary = QTextEdit()
        self.critical_errors_summary.setReadOnly(
            True
        )
        self.critical_errors_summary.setPlaceholderText(
            "No critical errors have been added yet."
        )

        critical_errors_layout.addWidget(
            critical_errors_guidance
        )
        critical_errors_layout.addWidget(
            critical_error_task_label
        )

        critical_errors_layout.addWidget(
            self.critical_error_task_selector
        )
        critical_errors_layout.addWidget(
            critical_error_label
        )

        critical_errors_layout.addWidget(
            self.critical_error_input
        )

        critical_errors_layout.addWidget(
            critical_evidence_label
        )

        critical_errors_layout.addWidget(
            self.critical_error_evidence_input
        )

        critical_errors_layout.addWidget(
            self.add_critical_error_button
        )

        critical_errors_layout.addWidget(
            critical_errors_summary_label
        )

        critical_errors_layout.addWidget(
            self.critical_errors_summary
        )

        self.page_stack.addWidget(
            critical_errors_page
        )
        # -------------------------------------------------
        # Stage 6 - Observable Metrics
        # -------------------------------------------------

        metrics_page = QWidget()
        metrics_layout = QVBoxLayout(
            metrics_page
        )

        metrics_guidance = QLabel(
            "Define something an observer could actually see, hear, "
            "record or measure that demonstrates the selected success "
            "factor."
        )
        metrics_guidance.setWordWrap(
            True
        )

        metric_task_label = QLabel(
            "COLLECTIVE TASK"
        )
        metric_task_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.metric_task_selector = QComboBox()
        self.metric_task_selector.setPlaceholderText(
            "Select the collective task"
        )

        metric_success_factor_label = QLabel(
            "SUCCESS FACTOR"
        )
        metric_success_factor_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.metric_success_factor_selector = QComboBox()
        self.metric_success_factor_selector.setPlaceholderText(
            "Select the success factor"
        )

        observable_metric_label = QLabel(
            "OBSERVABLE OR MEASURABLE INDICATOR"
        )
        observable_metric_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.observable_metric_input = QTextEdit()
        self.observable_metric_input.setPlaceholderText(
            "e.g. Key coordinating decisions are communicated to all "
            "relevant cells within the required timeframe"
        )
        self.observable_metric_input.setMaximumHeight(
            100
        )

        self.add_observable_metric_button = QPushButton(
            "ADD OBSERVABLE METRIC"
        )
        self.add_observable_metric_button.setEnabled(
            False
        )

        metrics_summary_label = QLabel(
            "CTO OBSERVABLE METRICS"
        )
        metrics_summary_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.observable_metrics_summary = QTextEdit()
        self.observable_metrics_summary.setReadOnly(
            True
        )
        self.observable_metrics_summary.setPlaceholderText(
            "No observable metrics have been added yet."
        )

        metrics_layout.addWidget(
            metrics_guidance
        )
        metrics_layout.addWidget(
            metric_task_label
        )
        metrics_layout.addWidget(
            self.metric_task_selector
        )
        metrics_layout.addWidget(
            metric_success_factor_label
        )
        metrics_layout.addWidget(
            self.metric_success_factor_selector
        )
        metrics_layout.addWidget(
            observable_metric_label
        )
        metrics_layout.addWidget(
            self.observable_metric_input
        )
        metrics_layout.addWidget(
            self.add_observable_metric_button
        )
        metrics_layout.addWidget(
            metrics_summary_label
        )
        metrics_layout.addWidget(
            self.observable_metrics_summary
        )

        self.page_stack.addWidget(
            metrics_page
        )

        # -------------------------------------------------
        # Stage 7 - Evidence Requirements
        # -------------------------------------------------

        evidence_page = QWidget()
        evidence_layout = QVBoxLayout(
            evidence_page
        )

        evidence_guidance = QLabel(
            "Define the evidence required to support a professional "
            "judgement against a specific observable metric."
        )
        evidence_guidance.setWordWrap(
            True
        )

        evidence_task_label = QLabel(
            "COLLECTIVE TASK"
        )
        evidence_task_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.evidence_task_selector = QComboBox()
        self.evidence_task_selector.setPlaceholderText(
            "Select the collective task"
        )

        evidence_success_factor_label = QLabel(
            "SUCCESS FACTOR"
        )
        evidence_success_factor_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.evidence_success_factor_selector = QComboBox()
        self.evidence_success_factor_selector.setPlaceholderText(
            "Select the success factor"
        )

        evidence_metric_label = QLabel(
            "OBSERVABLE METRIC"
        )
        evidence_metric_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.evidence_metric_selector = QComboBox()
        self.evidence_metric_selector.setPlaceholderText(
            "Select the observable metric"
        )

        evidence_description_label = QLabel(
            "EVIDENCE REQUIRED"
        )
        evidence_description_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.evidence_description_input = QTextEdit()
        self.evidence_description_input.setPlaceholderText(
            "e.g. Decision log showing the time, decision, owner "
            "and affected cells"
        )
        self.evidence_description_input.setMaximumHeight(
            100
        )

        evidence_type_label = QLabel(
            "EVIDENCE TYPE"
        )
        evidence_type_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.evidence_type_input = QLineEdit()
        self.evidence_type_input.setPlaceholderText(
            "e.g. Observation, decision log, message, record, artefact"
        )

        evidence_notes_label = QLabel(
            "NOTES (OPTIONAL)"
        )
        evidence_notes_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.evidence_notes_input = QTextEdit()
        self.evidence_notes_input.setPlaceholderText(
            "Add any quality, timing or collection notes..."
        )
        self.evidence_notes_input.setMaximumHeight(
            80
        )

        self.add_evidence_requirement_button = QPushButton(
            "ADD EVIDENCE REQUIREMENT"
        )
        self.add_evidence_requirement_button.setEnabled(
            False
        )

        evidence_summary_label = QLabel(
            "CTO EVIDENCE REQUIREMENTS"
        )
        evidence_summary_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.evidence_requirements_summary = QTextEdit()
        self.evidence_requirements_summary.setReadOnly(
            True
        )
        self.evidence_requirements_summary.setPlaceholderText(
            "No evidence requirements have been added yet."
        )

        evidence_layout.addWidget(
            evidence_guidance
        )
        evidence_layout.addWidget(
            evidence_task_label
        )
        evidence_layout.addWidget(
            self.evidence_task_selector
        )
        evidence_layout.addWidget(
            evidence_success_factor_label
        )
        evidence_layout.addWidget(
            self.evidence_success_factor_selector
        )
        evidence_layout.addWidget(
            evidence_metric_label
        )
        evidence_layout.addWidget(
            self.evidence_metric_selector
        )
        evidence_layout.addWidget(
            evidence_description_label
        )
        evidence_layout.addWidget(
            self.evidence_description_input
        )
        evidence_layout.addWidget(
            evidence_type_label
        )
        evidence_layout.addWidget(
            self.evidence_type_input
        )
        evidence_layout.addWidget(
            evidence_notes_label
        )
        evidence_layout.addWidget(
            self.evidence_notes_input
        )
        evidence_layout.addWidget(
            self.add_evidence_requirement_button
        )
        evidence_layout.addWidget(
            evidence_summary_label
        )
        evidence_layout.addWidget(
            self.evidence_requirements_summary
        )

        self.page_stack.addWidget(
            evidence_page
        )

        # -------------------------------------------------
        # Stage 8 - Design Review
        # -------------------------------------------------

        review_page = QWidget()

        review_layout = QVBoxLayout(
            review_page
        )

        self.design_review_text = QTextEdit()
        self.design_review_text.setReadOnly(
            True
        )

        review_layout.addWidget(
            self.design_review_text
        )

        self.page_stack.addWidget(
            review_page
        )

        work_layout.addWidget(
            self.page_stack
        )

        # -------------------------------------------------
        # Navigation buttons
        # -------------------------------------------------

        button_layout = QHBoxLayout()

        self.back_button = QPushButton(
            "BACK"
        )

        self.next_button = QPushButton(
            "NEXT"
        )

        button_layout.addWidget(
            self.back_button
        )

        button_layout.addStretch()

        button_layout.addWidget(
            self.next_button
        )

        work_layout.addLayout(
            button_layout
        )

        main_layout.addWidget(
            work_frame,
            3,
        )

        # -------------------------------------------------
        # Connections
        # -------------------------------------------------

        self.stage_list.currentRowChanged.connect(
            self._show_stage
        )

        self.back_button.clicked.connect(
            self._previous_stage
        )

        self.next_button.clicked.connect(
            self._next_stage
        )

        # -------------------------------------------------
        # Initial state
        # -------------------------------------------------

        self.stage_list.setCurrentRow(
            0
        )

        self._show_stage(
            0
        )

    def _refresh_metric_task_selector(
        self,
    ):
        current_index = (
            self.metric_task_selector
            .currentIndex()
        )

        self.metric_task_selector.blockSignals(
            True
        )

        self.metric_task_selector.clear()

        for task in self.cto.collective_tasks:
            self.metric_task_selector.addItem(
                task.title
            )

        if (
            current_index >= 0
            and current_index
            < self.metric_task_selector.count()
        ):
            self.metric_task_selector.setCurrentIndex(
                current_index
            )
        elif self.metric_task_selector.count() > 0:
            self.metric_task_selector.setCurrentIndex(
                0
            )

        self.metric_task_selector.blockSignals(
            False
        )

        self._refresh_metric_success_factor_selector()

    def _refresh_metric_success_factor_selector(
        self,
        *_ ,
    ):
        self.metric_success_factor_selector.blockSignals(
            True
        )
        self.metric_success_factor_selector.clear()

        task_index = (
            self.metric_task_selector
            .currentIndex()
        )

        if (
            task_index >= 0
            and task_index < len(self.cto.collective_tasks)
        ):
            selected_task = self.cto.collective_tasks[
                task_index
            ]

            for factor in selected_task.success_factors:
                self.metric_success_factor_selector.addItem(
                    factor.description
                )

            if self.metric_success_factor_selector.count() > 0:
                self.metric_success_factor_selector.setCurrentIndex(
                    0
                )

        self.metric_success_factor_selector.blockSignals(
            False
        )

        self._update_add_observable_metric_button()

    def _update_add_observable_metric_button(
        self,
        *_ ,
    ):
        has_task = (
            self.metric_task_selector.currentIndex() >= 0
        )
        has_success_factor = (
            self.metric_success_factor_selector.currentIndex() >= 0
        )
        has_metric = bool(
            self.observable_metric_input
            .toPlainText()
            .strip()
        )

        self.add_observable_metric_button.setEnabled(
            has_task
            and has_success_factor
            and has_metric
        )

    def _add_observable_metric(self):
        task_index = (
            self.metric_task_selector
            .currentIndex()
        )
        factor_index = (
            self.metric_success_factor_selector
            .currentIndex()
        )

        if (
            task_index < 0
            or task_index >= len(self.cto.collective_tasks)
        ):
            return

        selected_task = self.cto.collective_tasks[
            task_index
        ]

        if (
            factor_index < 0
            or factor_index >= len(selected_task.success_factors)
        ):
            return

        description = (
            self.observable_metric_input
            .toPlainText()
            .strip()
        )

        if not description:
            return

        selected_factor = selected_task.success_factors[
            factor_index
        ]

        selected_factor.metrics.append(
            PerformanceMetric(
                description=description,
                category="Success Factor",
            )
        )

        self.observable_metric_input.clear()

        self._refresh_observable_metrics_summary()
        self._refresh_evidence_task_selector()
        self._update_add_observable_metric_button()

    def _refresh_observable_metrics_summary(self):
        lines = []
        metric_number = 1

        for task in self.cto.collective_tasks:
            for factor in task.success_factors:
                for metric in factor.metrics:
                    lines.append(
                        f"{metric_number}. {task.title}"
                    )
                    lines.append(
                        f"   Success Factor: {factor.description}"
                    )
                    lines.append(
                        f"   Observable Metric: {metric.description}"
                    )
                    lines.append("")
                    metric_number += 1

        if not lines:
            self.observable_metrics_summary.setPlainText(
                "No observable metrics have been added yet."
            )
            return

        self.observable_metrics_summary.setPlainText(
            "\n".join(lines).strip()
        )

    def _refresh_critical_error_task_selector(
        self,
    ):
        current_index = (
            self.critical_error_task_selector
            .currentIndex()
        )

        self.critical_error_task_selector.blockSignals(
            True
        )

        self.critical_error_task_selector.clear()

        for task in self.cto.collective_tasks:
            self.critical_error_task_selector.addItem(
                task.title
            )

        if (
            current_index >= 0
            and current_index
            < self.critical_error_task_selector.count()
        ):
            self.critical_error_task_selector.setCurrentIndex(
                current_index
            )

        elif (
            self.critical_error_task_selector.count()
            > 0
        ):
            self.critical_error_task_selector.setCurrentIndex(
                0
            )

        self.critical_error_task_selector.blockSignals(
            False
        )

        self._update_add_critical_error_button()

    def _update_add_critical_error_button(
        self,
        *_,
    ):
        has_task = (
            self.critical_error_task_selector.currentIndex() >= 0
        )

        has_error = bool(
            self.critical_error_input
            .toPlainText()
            .strip()
        )

        has_evidence = bool(
            self.critical_error_evidence_input
            .toPlainText()
            .strip()
        )

        self.add_critical_error_button.setEnabled(
            has_task
            and has_error
            and has_evidence
        )

    def _add_critical_error(self):
        task_index = (
            self.critical_error_task_selector
            .currentIndex()
        )

        if task_index < 0:
            return

        if task_index >= len(
            self.cto.collective_tasks
        ):
            return

        selected_task = (
            self.cto.collective_tasks[
                task_index
            ]
        )

        error_description = (
            self.critical_error_input
            .toPlainText()
            .strip()
        )

        evidence_description = (
            self.critical_error_evidence_input
            .toPlainText()
            .strip()
        )

        if not error_description:
            return

        if not evidence_description:
            return

        critical_error = CriticalError(
            description=error_description
        )

        metric = PerformanceMetric(
            description=evidence_description,
            category="Critical Error",
        )

        metric.evidence_requirements.append(
            EvidenceRequirement(
                description=evidence_description
            )
        )

        critical_error.metrics.append(
            metric
        )

        selected_task.critical_errors.append(
            critical_error
        )

        self.critical_error_input.clear()
        self.critical_error_evidence_input.clear()

        self._refresh_critical_errors_summary()
        self._update_add_critical_error_button()

    def _refresh_critical_errors_summary(self):
        errors = []

        for task in self.cto.collective_tasks:
            for error in task.critical_errors:
                errors.append(
                    (
                        task,
                        error,
                    )
                )

        if not errors:
            self.critical_errors_summary.setPlainText(
                "No critical errors have been added yet."
            )
            return

        lines = []

        for index, (task, error) in enumerate(
            errors,
            start=1,
        ):
            lines.append(
                f"{index}. {task.title}"
            )

            lines.append(
                f"   Critical Error: {error.description}"
            )

            for metric in error.metrics:
                lines.append(
                    f"   Evidence: {metric.description}"
                )

            lines.append("")

        self.critical_errors_summary.setPlainText(
            "\n".join(lines).strip()
        )

    def _update_add_collective_task_button(
        self,
        *_,
    ):
        has_title = bool(
            self.collective_task_input
            .text()
            .strip()
        )

        has_success_factor = bool(
            self.current_collective_task
            and self.current_collective_task.success_factors
        )

        self.add_collective_task_button.setEnabled(
            has_title and has_success_factor
        )

    def _refresh_cto_tasks_summary(self):
        if not self.cto.collective_tasks:
            self.cto_tasks_summary.setPlainText(
                "No collective tasks have been added yet."
            )
            return

        lines = []

        for index, task in enumerate(
            self.cto.collective_tasks,
            start=1,
        ):
            lines.append(
                f"{index}. {task.title}"
            )

            for factor in task.success_factors:
                lines.append(
                    f"   - {factor.description}"
                )

            lines.append("")

        self.cto_tasks_summary.setPlainText(
            "\n".join(lines).strip()
        )

    def _update_training_audience(
        self,
        text: str,
    ):
        self.cto.training_audience = (
            text.strip()
        )
    def _update_collective_outcome(self):
        self.cto.required_outcome = (
            self.collective_outcome_input
            .toPlainText()
            .strip()
        )
    def _update_conditions(self):
        self.cto.conditions = (
            self.conditions_input
            .toPlainText()
            .strip()
        )
    def _update_challenge_level(
        self,
        value: int,
    ):
        if value == 0:
            self.cto.challenge_level = None
        else:
            self.cto.challenge_level = value
    def _show_stage(
        self,
        row: int,
    ):
        if row < 0:
            return

        self.page_stack.setCurrentIndex(
            row
        )

        titles = [
            "Training Audience",
            "Collective Outcome",
            "Conditions & Challenge",
            "Collective Tasks & Success",
            "Critical Errors",
            "Observable Metrics",
            "Evidence Requirements",
            "CTO Design Review",
        ]

        guidance = [
            (
                "Identify the collective whose performance "
                "is being developed or assessed."
            ),
            (
                "Describe what the collective must achieve "
                "together, rather than what one individual "
                "must know or do."
            ),
            (
                "Describe the circumstances, constraints, "
                "environment and level of challenge in which "
                "the collective must perform."
            ),
            (
                "Identify the collective tasks and the "
                "performance that would indicate success."
            ),
            (
                "Identify failures or actions serious enough "
                "to undermine successful collective "
                "performance."
            ),
            (
                "Define observable or measurable indicators "
                "that allow performance to be recognised."
            ),
            (
                "Define the evidence needed to justify a "
                "professional judgement about performance."
            ),
            (
                "Review the CTO structure, evidence coverage "
                "and identified design gaps before exercise "
                "design begins."
            ),
        ]

        self.page_title.setText(
            titles[row]
        )

        self.guidance_label.setText(
            guidance[row]
        )

        if row == 6:
            self._refresh_evidence_task_selector()
            self._refresh_evidence_requirements_summary()

        if row == 7:
            self._refresh_design_review()

        self._update_navigation_buttons()

    def _refresh_evidence_task_selector(
        self,
        *_,
    ):
        current_task = self.evidence_task_selector.currentData()

        self.evidence_task_selector.blockSignals(
            True
        )
        self.evidence_task_selector.clear()

        for task in self.cto.collective_tasks:
            if any(
                factor.metrics
                for factor in task.success_factors
            ):
                self.evidence_task_selector.addItem(
                    task.title,
                    task,
                )

        if current_task is not None:
            for index in range(
                self.evidence_task_selector.count()
            ):
                if (
                    self.evidence_task_selector.itemData(index)
                    is current_task
                ):
                    self.evidence_task_selector.setCurrentIndex(
                        index
                    )
                    break
            else:
                if self.evidence_task_selector.count() > 0:
                    self.evidence_task_selector.setCurrentIndex(
                        0
                    )
        elif self.evidence_task_selector.count() > 0:
            self.evidence_task_selector.setCurrentIndex(
                0
            )

        self.evidence_task_selector.blockSignals(
            False
        )

        self._refresh_evidence_success_factor_selector()

    def _refresh_evidence_success_factor_selector(
        self,
        *_,
    ):
        current_factor = (
            self.evidence_success_factor_selector.currentData()
        )

        self.evidence_success_factor_selector.blockSignals(
            True
        )
        self.evidence_success_factor_selector.clear()

        task = self.evidence_task_selector.currentData()

        if task is not None:
            for factor in task.success_factors:
                if factor.metrics:
                    self.evidence_success_factor_selector.addItem(
                        factor.description,
                        factor,
                    )

        if current_factor is not None:
            for index in range(
                self.evidence_success_factor_selector.count()
            ):
                if (
                    self.evidence_success_factor_selector.itemData(index)
                    is current_factor
                ):
                    self.evidence_success_factor_selector.setCurrentIndex(
                        index
                    )
                    break
            else:
                if self.evidence_success_factor_selector.count() > 0:
                    self.evidence_success_factor_selector.setCurrentIndex(
                        0
                    )
        elif self.evidence_success_factor_selector.count() > 0:
            self.evidence_success_factor_selector.setCurrentIndex(
                0
            )

        self.evidence_success_factor_selector.blockSignals(
            False
        )

        self._refresh_evidence_metric_selector()

    def _refresh_evidence_metric_selector(
        self,
        *_,
    ):
        current_metric = self.evidence_metric_selector.currentData()

        self.evidence_metric_selector.blockSignals(
            True
        )
        self.evidence_metric_selector.clear()

        factor = self.evidence_success_factor_selector.currentData()

        if factor is not None:
            for metric in factor.metrics:
                self.evidence_metric_selector.addItem(
                    metric.description,
                    metric,
                )

        if current_metric is not None:
            for index in range(
                self.evidence_metric_selector.count()
            ):
                if (
                    self.evidence_metric_selector.itemData(index)
                    is current_metric
                ):
                    self.evidence_metric_selector.setCurrentIndex(
                        index
                    )
                    break
            else:
                if self.evidence_metric_selector.count() > 0:
                    self.evidence_metric_selector.setCurrentIndex(
                        0
                    )
        elif self.evidence_metric_selector.count() > 0:
            self.evidence_metric_selector.setCurrentIndex(
                0
            )

        self.evidence_metric_selector.blockSignals(
            False
        )

        self._update_add_evidence_requirement_button()

    def _update_add_evidence_requirement_button(
        self,
        *_,
    ):
        has_metric = (
            self.evidence_metric_selector.currentData()
            is not None
        )

        has_description = bool(
            self.evidence_description_input
            .toPlainText()
            .strip()
        )

        has_type = bool(
            self.evidence_type_input
            .text()
            .strip()
        )

        self.add_evidence_requirement_button.setEnabled(
            has_metric
            and has_description
            and has_type
        )

    def _add_evidence_requirement(self):
        metric = self.evidence_metric_selector.currentData()

        if metric is None:
            return

        description = (
            self.evidence_description_input
            .toPlainText()
            .strip()
        )
        evidence_type = (
            self.evidence_type_input
            .text()
            .strip()
        )
        notes = (
            self.evidence_notes_input
            .toPlainText()
            .strip()
        )

        if not description or not evidence_type:
            return

        metric.evidence_requirements.append(
            EvidenceRequirement(
                description=description,
                evidence_type=evidence_type,
                notes=notes,
            )
        )

        self.evidence_description_input.clear()
        self.evidence_type_input.clear()
        self.evidence_notes_input.clear()

        self._refresh_evidence_requirements_summary()
        self._update_add_evidence_requirement_button()

    def _refresh_evidence_requirements_summary(self):
        lines = []
        requirement_number = 1

        for task in self.cto.collective_tasks:
            for factor in task.success_factors:
                for metric in factor.metrics:
                    for requirement in metric.evidence_requirements:
                        lines.append(
                            f"{requirement_number}. {task.title}"
                        )
                        lines.append(
                            f"   Success Factor: {factor.description}"
                        )
                        lines.append(
                            f"   Observable Metric: {metric.description}"
                        )
                        lines.append(
                            f"   Evidence: {requirement.description}"
                        )
                        lines.append(
                            f"   Type: {requirement.evidence_type or '-'}"
                        )
                        if requirement.notes:
                            lines.append(
                                f"   Notes: {requirement.notes}"
                            )
                        lines.append("")
                        requirement_number += 1

        if not lines:
            self.evidence_requirements_summary.setPlainText(
                "No evidence requirements have been added yet."
            )
            return

        self.evidence_requirements_summary.setPlainText(
            "\n".join(lines).strip()
        )

    def _refresh_design_review(self):
        reasons = self.cto.collective_test_reasons()

        success_gaps = []
        critical_gaps = []
        advisories = []

        # -------------------------------------------------
        # Success-factor assurance gaps
        # -------------------------------------------------

        for task in self.cto.collective_tasks:
            for factor in task.success_factors:
                if not factor.metrics:
                    success_gaps.append(
                        (
                            task.title,
                            factor.description,
                            None,
                            "No observable metric defined.",
                        )
                    )
                    continue

                for metric in factor.metrics:
                    if not metric.evidence_requirements:
                        success_gaps.append(
                            (
                                task.title,
                                factor.description,
                                metric.description,
                                "No evidence requirement defined.",
                            )
                        )

        # -------------------------------------------------
        # Critical-error assurance gaps
        # -------------------------------------------------

        for task in self.cto.collective_tasks:
            for error in task.critical_errors:
                if not error.metrics:
                    critical_gaps.append(
                        (
                            task.title,
                            error.description,
                            None,
                            "No observable metric defined for critical error.",
                        )
                    )
                    continue

                for metric in error.metrics:
                    if not metric.evidence_requirements:
                        critical_gaps.append(
                            (
                                task.title,
                                error.description,
                                metric.description,
                                "No evidence requirement defined for critical-error metric.",
                            )
                        )

        # -------------------------------------------------
        # Advisory observations
        # -------------------------------------------------

        if not self.cto.conditions.strip():
            advisories.append(
                "No conditions have been defined. Consider whether the "
                "performance context, constraints or environment should "
                "be made explicit."
            )

        if self.cto.challenge_level is None:
            advisories.append(
                "No challenge level has been specified. This is acceptable "
                "where the training methodology does not require one."
            )

        if not self.cto.critical_errors():
            advisories.append(
                "No critical errors have been identified. This does not "
                "block exercise design, but consider whether any failure "
                "would be serious enough to require explicit observation."
            )

        structure_complete = (
            self.cto.passes_collective_structure_test()
        )
        success_complete = (
            self.cto.has_evidence_coverage()
        )
        critical_complete = (
            self.cto.has_critical_error_coverage()
        )

        ready = (
            structure_complete
            and success_complete
            and critical_complete
        )

        lines = [
            "CTO DESIGN REVIEW",
            "",
            "TRAINING AUDIENCE",
            self.cto.training_audience or "-",
            "",
            "REQUIRED COLLECTIVE OUTCOME",
            self.cto.required_outcome or "-",
            "",
            "CONDITIONS",
            self.cto.conditions or "-",
            "",
            "CHALLENGE LEVEL",
            (
                str(self.cto.challenge_level)
                if self.cto.challenge_level is not None
                else "Not specified"
            ),
            "",
            "COLLECTIVE STRUCTURE",
            (
                "Complete"
                if structure_complete
                else "Needs development"
            ),
        ]

        if reasons:
            for reason in reasons:
                lines.append(
                    f"  - {reason}"
                )

        lines.extend(
            [
                "",
                "SUCCESS EVIDENCE COVERAGE",
                (
                    "Complete"
                    if success_complete
                    else "Needs development"
                ),
                "",
                "CRITICAL ERROR COVERAGE",
                (
                    "Complete"
                    if critical_complete
                    else "Needs development"
                ),
                "",
                "ASSURANCE GAPS",
            ]
        )

        if not reasons and not success_gaps and not critical_gaps:
            lines.append(
                "None identified"
            )
        else:
            if reasons:
                lines.append(
                    "Collective Structure"
                )
                for reason in reasons:
                    lines.append(
                        f"  - {reason}"
                    )
                lines.append("")

            for task_title, factor_description, metric_description, gap in success_gaps:
                lines.append(
                    f"Collective Task: {task_title}"
                )
                lines.append(
                    f"  Success Factor: {factor_description}"
                )
                if metric_description:
                    lines.append(
                        f"  Observable Metric: {metric_description}"
                    )
                lines.append(
                    f"  GAP: {gap}"
                )
                lines.append("")

            for task_title, error_description, metric_description, gap in critical_gaps:
                lines.append(
                    f"Collective Task: {task_title}"
                )
                lines.append(
                    f"  Critical Error: {error_description}"
                )
                if metric_description:
                    lines.append(
                        f"  Observable Metric: {metric_description}"
                    )
                lines.append(
                    f"  GAP: {gap}"
                )
                lines.append("")

        lines.extend(
            [
                "",
                "ADVISORY OBSERVATIONS",
            ]
        )

        if advisories:
            for advisory in advisories:
                lines.append(
                    f"  - {advisory}"
                )
        else:
            lines.append(
                "None identified"
            )

        lines.extend(
            [
                "",
                "DESIGN STATUS",
                (
                    "READY FOR EXERCISE DESIGN"
                    if ready
                    else "NEEDS DEVELOPMENT"
                ),
            ]
        )

        if ready:
            lines.extend(
                [
                    "",
                    (
                        "The CTO meets the current structural and evidence "
                        "coverage checks. This is an assurance gate for "
                        "progression into exercise design; professional "
                        "judgement remains with the Exercise Director."
                    ),
                ]
            )
        else:
            lines.extend(
                [
                    "",
                    (
                        "Resolve the assurance gaps above before treating "
                        "the CTO as ready for exercise design."
                    ),
                ]
            )

        self.design_review_text.setPlainText(
            "\n".join(lines)
        )

    def _previous_stage(self):
        row = self.stage_list.currentRow()

        if row > 0:
            self.stage_list.setCurrentRow(
                row - 1
            )

    def _next_stage(self):
        row = self.stage_list.currentRow()

        if row < self.stage_list.count() - 1:
            self.stage_list.setCurrentRow(
                row + 1
            )

    def _update_navigation_buttons(self):
        row = self.stage_list.currentRow()

        self.back_button.setEnabled(
            row > 0
        )

        self.next_button.setEnabled(
            row < self.stage_list.count() - 1
        )
    def _ensure_current_collective_task(self):
        task_title = (
            self.collective_task_input
            .text()
            .strip()
        )

        if not task_title:
            return None

        if self.current_collective_task is None:
            self.current_collective_task = CollectiveTask(
                title=task_title
            )
        else:
            self.current_collective_task.title = (
                task_title
            )
        return self.current_collective_task

    def _add_success_factor(self):
        task = self._ensure_current_collective_task()

        if task is None:
            return

        description = (
            self.success_factor_input
            .toPlainText()
            .strip()
        )

        if not description:
            return

        task.success_factors.append(
            SuccessFactor(
                description=description
            )
        )

        self.success_factor_input.clear()

        self._refresh_current_task_summary()
        self._update_add_collective_task_button()


    def _add_collective_task(self):
        task = self._ensure_current_collective_task()

        if task is None:
            return

        self.cto.collective_tasks.append(
            task
        )

        self.current_collective_task = None

        self.collective_task_input.clear()
        self.success_factor_input.clear()

        self._refresh_current_task_summary()
        self._refresh_cto_tasks_summary()
        self._refresh_critical_error_task_selector()
        self._refresh_metric_task_selector()
        self._refresh_observable_metrics_summary()
        self._refresh_evidence_task_selector()
        self._update_add_collective_task_button()
    def _refresh_current_task_summary(self):
        task = self.current_collective_task

        if task is None:
            self.current_task_summary.setPlainText(
                "No collective task is currently being developed."
            )
            return

        lines = [
            task.title,
        ]

        for factor in task.success_factors:
            lines.append(
                f"- {factor.description}"
            )

        self.current_task_summary.setPlainText(
            "\n".join(lines)
        )
