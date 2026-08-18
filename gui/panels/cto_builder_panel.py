from PySide6.QtWidgets import (
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

        # -------------------------------------------------
        # Stages 5-7 - placeholders for later bricks
        # -------------------------------------------------

        for _ in range(3):
            page = QWidget()

            page_layout = QVBoxLayout(
                page
            )

            placeholder = QTextEdit()
            placeholder.setReadOnly(
                True
            )
            placeholder.setPlaceholderText(
                "This CTO Builder stage will be added "
                "in the next development brick."
            )

            page_layout.addWidget(
                placeholder
            )

            self.page_stack.addWidget(
                page
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

        if row == 7:
            self._refresh_design_review()

        self._update_navigation_buttons()

    def _refresh_design_review(self):
        reasons = (
            self.cto.collective_test_reasons()
        )

        lines = [
            "CTO DESIGN REVIEW",
            "",
            "TRAINING AUDIENCE",
            (
                self.cto.training_audience
                or "-"
            ),
            "",
            "REQUIRED COLLECTIVE OUTCOME",
            (
                self.cto.required_outcome
                or "-"
            ),
            "",
            "CONDITIONS",
            (
                self.cto.conditions
                or "-"
            ),
            "",
            "CHALLENGE LEVEL",
            (
                str(self.cto.challenge_level)
                if self.cto.challenge_level is not None
                else "Not specified"
            ),
            "",
            "COLLECTIVE STRUCTURE",
        ]

        if reasons:
            for reason in reasons:
                lines.append(
                    f"- {reason}"
                )
        else:
            lines.append(
                "Complete"
            )

        lines.extend(
            [
                "",
                "SUCCESS EVIDENCE COVERAGE",
                (
                    "Complete"
                    if self.cto.has_evidence_coverage()
                    else "Needs development"
                ),
                "",
                "CRITICAL ERROR COVERAGE",
                (
                    "Complete"
                    if self.cto.has_critical_error_coverage()
                    else "Needs development"
                ),
                "",
                "DESIGN STATUS",
            ]
        )

        if (
            self.cto.passes_collective_structure_test()
            and self.cto.has_evidence_coverage()
            and self.cto.has_critical_error_coverage()
        ):
            lines.append(
                "Ready for Exercise Design"
            )
        else:
            lines.append(
                "Needs Development"
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
