from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
    QScrollArea,
    QMessageBox,
)
from core import objective
from core.design_assistance import DesignAssistance
from core.design_assistance import (
    DesignAssistance,
    DesignOptionType,
)
from core.design_proposal_builder import (
    DesignProposalBuilder,
)
from core.design_proposal_applier import (
    DesignProposalApplier,
)
from core.design_trace_builder import (
    DesignTraceBuilder,
)
from core.design_proposal import (
    DesignProposalStatus,
)


class DesignerWorkspacePanel(QWidget):
    """
    Read-only designer workspace.

    Presents the relationship between exercise objectives,
    success criteria and supporting MEL/MIL activity without
    requiring the designer to understand the underlying
    project data model.
    """

    open_in_workspace_requested = Signal(int)

    def __init__(self):
        super().__init__()

        self.project = None
        self.selected_objective = None
        self.attention_items = []
        self.selected_attention_item = None
        self.current_design_proposal = None

        main_layout = QVBoxLayout(self)

        heading = QLabel("Designer Workspace")
        heading.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )
        main_layout.addWidget(heading)

        self.journey_label = QLabel(
            "PREPARE  →  RUN  →  UNDERSTAND  →  DECIDE"
        )
        self.journey_label.setStyleSheet(
            "font-size: 13px; font-weight: bold;"
        )
        main_layout.addWidget(self.journey_label)

        question = QLabel(
            "What are we trying to achieve?"
        )
        question.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        main_layout.addWidget(question)
        
        self.attention_group = QGroupBox(
            "Needs Your Attention"
        )
        attention_layout = QVBoxLayout(
            self.attention_group
        )

        self.attention_summary = QLabel(
            "No design matters currently require attention."
        )
        self.attention_summary.setWordWrap(True)

        attention_layout.addWidget(
            self.attention_summary
        )

        self.attention_list = QListWidget()
        self.attention_list.currentRowChanged.connect(
            self._attention_selected
        )
        attention_layout.addWidget(
            self.attention_list
        )

        main_layout.addWidget(
            self.attention_group
        )

        content = QHBoxLayout()
        main_layout.addLayout(content, 1)

        objectives_group = QGroupBox(
            "Exercise Objectives"
        )
        objectives_layout = QVBoxLayout(
            objectives_group
        )

        self.objectives_summary = QLabel(
            "No exercise objectives have been defined."
        )
        self.objectives_summary.setWordWrap(True)
        objectives_layout.addWidget(
            self.objectives_summary
        )

        self.objectives_list = QListWidget()
        self.objectives_list.currentRowChanged.connect(
            self._objective_selected
        )
        self.objectives_list.itemClicked.connect(
            self._objective_clicked
        )
        objectives_layout.addWidget(
            self.objectives_list,
            1,
        )

        content.addWidget(objectives_group, 2)

        design_group = QGroupBox("Design Chain")
        self.design_layout = QVBoxLayout(design_group)

        self.design_chain = QLabel(
            "Select an objective to review its design chain."
        )
        self.design_chain.setWordWrap(True)
        self.design_chain.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.design_chain_scroll = QScrollArea()
        self.design_chain_scroll.setWidgetResizable(True)
        self.design_chain_scroll.setFrameShape(
            QScrollArea.Shape.NoFrame
        )
        self.design_chain_scroll.setWidget(
            self.design_chain
        )
        self.design_layout.addWidget(
        self.design_chain_scroll,
            1,

        )
        
        self.reviewed_content_label = QLabel(
            "YOUR REVIEWED VERSION"
        )
        self.reviewed_content_label.setStyleSheet(
            "font-weight: bold;"
        )
        self.reviewed_content_label.setVisible(False)

        self.design_layout.addWidget(
            self.reviewed_content_label
        )

        self.reviewed_content_editor = QPlainTextEdit()
        self.reviewed_content_editor.setPlaceholderText(
            "Enter one success criterion per line."
        )
        self.reviewed_content_editor.setVisible(False)
        self.reviewed_content_editor.setMinimumHeight(120)

        self.design_layout.addWidget(
            self.reviewed_content_editor
        )

        self.save_reviewed_content_button = QPushButton(
            "Save Reviewed Version"
        )
        self.accept_reviewed_content_button = QPushButton(
            "Accept Reviewed Version"
        )
        self.apply_proposal_button = QPushButton(
            "Apply to Design"
        )
        self.apply_proposal_button.setVisible(False)
        self.apply_proposal_button.clicked.connect(
            self._apply_design_proposal
        )

        self.design_layout.addWidget(
            self.apply_proposal_button
        )
        self.accept_reviewed_content_button.setVisible(False)
        self.accept_reviewed_content_button.clicked.connect(
            self._accept_reviewed_content
        )

        self.design_layout.addWidget(
            self.accept_reviewed_content_button
        )
        self.save_reviewed_content_button.setVisible(False)
        self.save_reviewed_content_button.clicked.connect(
            self._save_reviewed_content
        )

        self.design_layout.addWidget(
            self.save_reviewed_content_button
        )

        self.begin_proposal_review_button = QPushButton(
            "Begin Designer Review"
        )
        self.begin_proposal_review_button.setVisible(False)
        self.begin_proposal_review_button.clicked.connect(
            self._begin_proposal_review
        )
        self.design_layout.addWidget(
            self.begin_proposal_review_button
        )
        self.review_success_criteria_proposal_button = QPushButton(
            "Consider Defining Success Criteria"
        )
        self.review_success_criteria_proposal_button.setVisible(
            False
        )
        self.review_success_criteria_proposal_button.clicked.connect(
            self._review_success_criteria_proposal
        )
        self.design_layout.addWidget(
            self.review_success_criteria_proposal_button
        )

        self.review_supporting_activity_button = QPushButton(
            "Review Supporting Activity"
        )
        self.review_supporting_activity_button.setVisible(
            False
        )
        self.review_supporting_activity_button.clicked.connect(
            self._review_supporting_activity
        )
        self.design_layout.addWidget(
            self.review_supporting_activity_button
        )

        self.return_to_design_button = QPushButton(
            "Return to Design Chain"
        )
        self.return_to_design_button.setVisible(False)
        self.return_to_design_button.clicked.connect(
            self._return_to_design_chain
        )
        self.design_layout.addWidget(
            self.return_to_design_button
        )

        self.open_button = QPushButton(
            "Open Supporting Activity"
        )
        self.open_button.setEnabled(False)
        self.open_button.clicked.connect(
            self._open_supporting_activity
        )
        self.design_layout.addWidget(
            self.open_button
        )

        content.addWidget(
            design_group,
            3,
        )
    def _accept_reviewed_content(self):
        proposal = self.current_design_proposal

        if proposal is None:
            return

        if (
            proposal.status
            is not DesignProposalStatus.UNDER_REVIEW
        ):
            return

        lines = (
            self.reviewed_content_editor
            .toPlainText()
            .splitlines()
        )

        proposal.replace_reviewed_content(lines)

        proposal.accept(
            reviewed_by="Exercise Designer"
        )

        self._show_design_proposal()
        
    def _apply_design_proposal(self):
        proposal = self.current_design_proposal

        if (
            proposal is None
            or self.selected_objective is None
        ):
            return

        applier = DesignProposalApplier()

        try:
            applier.apply(
                proposal,
                self.selected_objective,
            )
        except ValueError as error:
            QMessageBox.warning(
                self,
                "Apply Design Proposal",
                str(error),
            )
            return
        trace_builder = DesignTraceBuilder()

        trace_record = trace_builder.build_applied_record(
            proposal,
            self.selected_objective,
        )

        if self.project is not None:
            self.project.add_design_trace_record(
                trace_record
            )
            
        self.current_design_proposal = None
        self.selected_attention_item = None

        self._update_design_attention()
        self._show_selected_objective()

          
    def _save_reviewed_content(self):
        proposal = self.current_design_proposal

        if proposal is None:
            return

        lines = (
            self.reviewed_content_editor
            .toPlainText()
            .splitlines()
        )

        proposal.replace_reviewed_content(lines)

        self._show_design_proposal()

    def _review_supporting_activity(self):
        if self.selected_attention_item is None:
            return

        options = (
            self.selected_attention_item.options
            or []
        )

        has_review_option = any(
            option.option_type
            is DesignOptionType.REVIEW_SUPPORTING_ACTIVITY
            for option in options
        )

        if not has_review_option:
            return
        
        self._open_supporting_activity()

    def set_project(self, project):
        """
        Display the current project's objective design picture.
        """

        self.project = project
        self.selected_objective = None
        self.selected_attention_item = None
        self._update_design_attention()
        self.current_design_proposal = None

        self.objectives_list.clear()
        self.open_button.setEnabled(False)

        if project is None or not project.objectives:
            self.objectives_summary.setText(
                "No exercise objectives have been defined."
            )
            self.design_chain.setText(
                "Add an exercise objective to begin "
                "building the design chain."
            )
            return

        self.objectives_summary.setText(
            f"{len(project.objectives)} exercise objectives defined."
        )

        for number, objective in enumerate(
            project.objectives,
            start=1,
        ):
            title = (
                objective.title.strip()
                or "Untitled objective"
            )

            item = QListWidgetItem(
                f"{number}. {title}"
            )
            self.objectives_list.addItem(item)

        self.objectives_list.setCurrentRow(0)
    def _update_design_attention(self):
        self.attention_list.clear()
        self.attention_items = []

        if self.project is None:
            self.attention_summary.setText(
                "No project is currently loaded."
            )
            return

        items = DesignAssistance(
            self.project
        ).check()

        self.attention_items = items

        if not items:
            self.attention_summary.setText(
                "No design matters currently require attention."
            )
            return

        self.attention_summary.setText(
            f"{len(items)} design matter"
            f"{'' if len(items) == 1 else 's'} "
            "may require professional attention."
        )

        for item in items:
            text = (
                f"⚠ {item.objective_title}\n"
                f"{item.title}\n"
                f"{item.message}"
            )

            self.attention_list.addItem(
                QListWidgetItem(text)
            )
    def _attention_selected(self, row):
        if (
            row < 0
            or row >= len(self.attention_items)
        ):
            return

        item = self.attention_items[row]
        self.selected_attention_item = item

        if (
            item.objective_index < 0
            or self.project is None
            or item.objective_index
            >= len(self.project.objectives)
        ):
            return

        self.objectives_list.blockSignals(True)

        self.objectives_list.setCurrentRow(
            item.objective_index
        )

        self.objectives_list.blockSignals(False)

        self.selected_objective = (
            self.project.objectives[
                item.objective_index
            ]
        )

        self._show_selected_objective()
    def _objective_clicked(self, item):
        """
        Explicitly selecting an objective returns the designer
        to the normal Design Chain view.
        """
        
        row = self.objectives_list.row(item)

        if (
            self.project is None
            or row < 0
            or row >= len(self.project.objectives)
        ):
            return

        self.selected_objective = (
            self.project.objectives[row]
        )

        self.selected_attention_item = None

        self._show_selected_objective()
         
    def _objective_selected(self, row):
        if (
            self.project is None
            or row < 0
            or row >= len(self.project.objectives)
        ):
            self.selected_objective = None
            self.design_chain.setText(
                "Select an objective to review "
                "its design chain."
            )
            self.open_button.setEnabled(False)
            return

        objective = self.project.objectives[row]
        self.selected_objective = objective

        self.selected_attention_item = None
        self._show_selected_objective()
    def _return_to_design_chain(self):
        """
        Return from the current review layer.

        Proposal Review returns to Contextual Review.
        Contextual Review returns to the normal Design Chain.
        """

        if self.current_design_proposal is not None:
            self.current_design_proposal = None
            self._show_selected_objective()
            return

        self.selected_attention_item = None
        self._show_selected_objective()     
    def _show_selected_objective(self):
        if self.selected_objective is None:
            return

        objective = self.selected_objective

        self.return_to_design_button.setVisible(
            self.selected_attention_item is not None
        )
        self.accept_reviewed_content_button.setVisible(
            False
        )
        self.begin_proposal_review_button.setVisible(
            False
        )
        self.apply_proposal_button.setVisible(
            False
        )

        options = []

        if self.selected_attention_item is not None:
            options = (
                self.selected_attention_item.options
                or []
            )

        self.review_success_criteria_proposal_button.setVisible(
            any(
                option.option_type
                is DesignOptionType.DEFINE_SUCCESS_CRITERIA
                for option in options
            )
        )

        self.review_supporting_activity_button.setVisible(
            any(
                option.option_type
                is DesignOptionType.REVIEW_SUPPORTING_ACTIVITY
                for option in options
                
            )
        )

        success_criteria = getattr(
            objective,
            "success_criteria",
            [],
        )

        supporting_injects = getattr(
            objective,
            "supporting_injects",
            [],
        )

        if success_criteria:
            criteria_text = "\n".join(
                f"• {criterion}"
                for criterion in success_criteria
            )
        else:
            criteria_text = (
                "No success criteria currently defined."
            )

        inject_lines = []

        for inject_number in supporting_injects:
            inject = self._find_inject(
                inject_number
            )

            if inject is None:
                inject_lines.append(
                    f"• Inject {inject_number}"
                )
                continue

            exercise_time = (
                inject.exercise_time.strip()
                if inject.exercise_time
                else "Time not set"
            )

            title = (
                inject.title.strip()
                or "Untitled activity"
            )

            inject_lines.append(
                f"• Inject {inject_number} — "
                f"{exercise_time} — {title}"
            )

        if inject_lines:
            inject_text = "\n".join(
                inject_lines
            )
        else:
            inject_text = (
                "No supporting MEL/MIL activity "
                "currently identified."
            )

        doctrine = getattr(
            objective,
            "supporting_doctrine",
            [],
        )

        if doctrine:
            doctrine_text = "\n".join(
                f"• {reference}"
                for reference in doctrine
            )
        else:
            doctrine_text = (
                "No supporting doctrine currently linked."
            )

        context_text = ""

        if self.selected_attention_item is not None:
            item = self.selected_attention_item

            options_text = ""

            if item.options:
                option_lines = []

                for option in item.options:
                    option_lines.append(
                        f"• {option.title}\n"
                        f"  {option.description}"
                    )

                options_text = (
                    f"\n\nWHAT COULD I DO?\n"
                    f"{chr(10).join(option_lines)}"
                )

            context_text = (
                f"\n\nCONTEXTUAL REVIEW\n"
                f"⚠ {item.title}\n\n"
                f"WHAT EXERCISE DIRECTOR NOTICED\n"
                f"{item.message}\n\n"
                f"WHY THIS MATTERS\n"
                f"{item.rationale}"
                f"{options_text}\n\n"
                f"Exercise Director has identified a "
                f"design condition for professional review. "
                f"It has not selected an option or made an "
                f"assessment of whether the objective itself "
                f"is appropriate."
            )

        self.design_chain.setText(
            f"WHY?\n"
            f"{objective.title}\n\n"
            f"WHAT MUST THEY DEMONSTRATE?\n"
            f"{criteria_text}\n\n"
            f"HOW WILL WE CREATE THE OPPORTUNITY?\n"
            f"{inject_text}\n\n"
            f"WHAT SUPPORTS THE DESIGN?\n"
            f"{doctrine_text}"
            f"{context_text}"
        )

        self.open_button.setEnabled(
            bool(supporting_injects)
        )

    def _review_success_criteria_proposal(self):
        if (
            self.project is None
            or self.selected_objective is None
            or self.selected_attention_item is None
        ):
            return

        options = (
            self.selected_attention_item.options
            or []
        )

        has_proposal_option = any(
            option.option_type
            is DesignOptionType.DEFINE_SUCCESS_CRITERIA
            for option in options
        )

        if not has_proposal_option:
            return

        proposal = DesignProposalBuilder(
            self.project
        ).build_success_criteria_proposal(
            self.selected_objective
        )

        trace_record = (
            DesignTraceBuilder()
            .build_proposal_created_record(
                proposal
            )
        )

        self.project.add_design_trace_record(
            trace_record
        )

        self.current_design_proposal = proposal

        self._show_design_proposal()
        
    def _begin_proposal_review(self):
        proposal = self.current_design_proposal

        if proposal is None:
            return

        proposal.begin_review()

        self._show_design_proposal()
        
    def _show_design_proposal(self):
        proposal = self.current_design_proposal

        if proposal is None:
            return
        self.begin_proposal_review_button.setVisible(
            proposal.status
            is DesignProposalStatus.DRAFT
            )
        is_under_review = (
            proposal.status
            is DesignProposalStatus.UNDER_REVIEW
        )
        self.apply_proposal_button.setVisible(
            proposal.status
            is DesignProposalStatus.ACCEPTED
        )
        self.accept_reviewed_content_button.setVisible(
            is_under_review
        )
        
        self.reviewed_content_label.setVisible(
            is_under_review
            
        )
        self.reviewed_content_editor.setVisible(
            is_under_review
        )
        self.save_reviewed_content_button.setVisible(
            is_under_review
        )
        if is_under_review:
            self.reviewed_content_editor.setPlainText(
                "\n".join(
                    proposal.reviewed_content
                )
            )
        self.review_success_criteria_proposal_button.setVisible(
        False
        )
        
        self.return_to_design_button.setVisible(
            True
        )
        
        self.review_supporting_activity_button.setVisible(
        False
        )
        if proposal.sources:
            source_lines = []

            for source in proposal.sources:
                source_lines.append(
                    f"• {source.source_type} — "
                    f"{source.source_reference}\n"
                    f"  {source.source_text}"
                )

            sources_text = "\n".join(
                source_lines
            )
        else:
            sources_text = (
                "No supporting source material identified."
            )

        if proposal.proposed_content:
            proposal_lines = []

            for content in proposal.proposed_content:
                proposal_lines.append(
                    f"• {content}"
                )

            proposed_text = "\n".join(
                proposal_lines
            )
        else:
            proposed_text = (
                "Exercise Director could not derive candidate "
                "success criteria from the current supporting "
                "activity."
            )
        
        self.design_chain.setText(
            f"PROPOSED SUCCESS CRITERIA\n\n"
            f"Objective\n"
            f"{proposal.objective_title}\n\n"
            f"WHAT EXERCISE DIRECTOR CONSIDERED\n"
            f"{sources_text}\n\n"
            f"POSSIBLE DRAFT\n"
            f"{proposed_text}\n\n"
            f"WHY THIS WAS PROPOSED\n"
            f"{proposal.rationale}\n\n"
            f"STATUS\n"
            f"{proposal.status.value}\n\n"
            f"Authoritative design remains unchanged."
        )

        self.review_success_criteria_proposal_button.setVisible(
            False
        )

        self.review_supporting_activity_button.setVisible(
            False
        )

        self.return_to_design_button.setVisible(
            True
        )
    def _find_inject(self, inject_number):
        if self.project is None:
            return None

        for inject in self.project.injects:
            if inject.number == inject_number:
                return inject

        return None

    def _open_supporting_activity(self):
        if self.selected_objective is None:
            return

        supporting_injects = getattr(
            self.selected_objective,
            "supporting_injects",
            [],
        )

        if not supporting_injects:
            return

        self.open_in_workspace_requested.emit(
            supporting_injects[0]
        )