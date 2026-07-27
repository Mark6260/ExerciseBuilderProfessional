from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ExerciseDefinitionDialog(QDialog):
    """
    Guides the Exercise Director through an initial
    Readiness Analysis before detailed exercise design begins.
    """

    PAGE_TITLES = [
        "Target Readiness",
        "Operational Requirement",
        "Current Readiness",
        "Required Standard",
        "Readiness Gap",
        "Training Audience",
        "Learning Opportunities",
        "Readiness Analysis Summary",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Readiness Analysis")
        self.resize(820, 650)

        self.current_page_index = 0

        self.stage_label = QLabel()
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, len(self.PAGE_TITLES))
        self.progress_bar.setTextVisible(False)

        self.pages = QStackedWidget()

        self.target_readiness_input = QTextEdit()
        self.operational_requirement_input = QTextEdit()
        self.current_readiness_input = QTextEdit()
        self.required_standard_input = QTextEdit()
        self.readiness_gap_input = QTextEdit()
        self.training_audience_input = QTextEdit()
        self.learning_opportunities_input = QTextEdit()

        self.summary_label = QLabel()
        self.summary_label.setWordWrap(True)

        self._create_pages()

        self.back_button = QPushButton("Back")
        self.next_button = QPushButton("Continue")
        self.cancel_button = QPushButton("Cancel")

        self.back_button.clicked.connect(
            self.previous_page
        )
        self.next_button.clicked.connect(
            self.next_page
        )
        self.cancel_button.clicked.connect(
            self.reject
        )

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.next_button)

        layout = QVBoxLayout()

        layout.addWidget(self.stage_label)
        layout.addWidget(self.progress_bar)
        layout.addSpacing(10)
        layout.addWidget(self.pages, 1)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self._update_navigation()

    def _create_pages(self):
        self.pages.addWidget(
            self._create_text_page(
                title="Tell me what readiness you're trying to achieve.",
                guidance=(
                    "Describe the level of readiness that the individual, "
                    "team, unit or organisation must reach.\n\n"
                    "Focus on the required outcome rather than the type "
                    "of exercise you intend to run."
                ),
                input_widget=self.target_readiness_input,
                placeholder=(
                    "Example: The Brigade must be ready to deploy "
                    "following successful completion of Foxtrot training."
                ),
            )
        )

        self.pages.addWidget(
            self._create_text_page(
                title="Why is this readiness required?",
                guidance=(
                    "Describe the operational requirement, organisational "
                    "need or progression requirement driving the training."
                ),
                input_widget=self.operational_requirement_input,
                placeholder=(
                    "Explain why this readiness is required and what "
                    "depends upon it."
                ),
            )
        )

        self.pages.addWidget(
            self._create_text_page(
                title="Where are they today?",
                guidance=(
                    "Describe the current readiness of the training "
                    "audience, including experience, qualifications, "
                    "recent training and known weaknesses."
                ),
                input_widget=self.current_readiness_input,
                placeholder=(
                    "Describe their present level of readiness..."
                ),
            )
        )

        self.pages.addWidget(
            self._create_text_page(
                title="How will you recognise that they are ready?",
                guidance=(
                    "Describe the required standard and the observable "
                    "outcomes that would justify progression to the "
                    "next readiness level."
                ),
                input_widget=self.required_standard_input,
                placeholder=(
                    "What would an instructor need to observe before "
                    "making a positive readiness decision?"
                ),
            )
        )

        self.pages.addWidget(
            self._create_text_page(
                title="What is preventing them from getting there?",
                guidance=(
                    "Identify the readiness gap. Consider knowledge, "
                    "skills, experience, judgement, teamwork, equipment, "
                    "integration, procedures and confidence."
                ),
                input_widget=self.readiness_gap_input,
                placeholder=(
                    "Describe the gaps between current and required "
                    "readiness..."
                ),
            )
        )

        self.pages.addWidget(
            self._create_text_page(
                title="Who must develop?",
                guidance=(
                    "Identify the individuals, teams, units or "
                    "organisations involved.\n\n"
                    "Include both collective and individual training "
                    "requirements where appropriate."
                ),
                input_widget=self.training_audience_input,
                placeholder=(
                    "Identify the primary and supporting training "
                    "audiences..."
                ),
            )
        )

        self.pages.addWidget(
            self._create_text_page(
                title="What learning opportunities are required?",
                guidance=(
                    "Consider exercises, practical serials, simulation, "
                    "workshops, coaching, mentoring, courses and other "
                    "activities that could reduce the readiness gap."
                ),
                input_widget=self.learning_opportunities_input,
                placeholder=(
                    "Describe the learning opportunities that may be "
                    "required..."
                ),
            )
        )

        summary_page = QWidget()
        summary_layout = QVBoxLayout(summary_page)

        summary_title = QLabel(
            "<h2>Readiness Analysis Summary</h2>"
        )

        summary_guidance = QLabel(
            "Review the analysis before creating the exercise."
        )
        summary_guidance.setWordWrap(True)

        self.summary_label.setTextFormat(
            self.summary_label.textFormat()
        )

        summary_layout.addWidget(summary_title)
        summary_layout.addWidget(summary_guidance)
        summary_layout.addSpacing(10)
        summary_layout.addWidget(self.summary_label, 1)

        self.pages.addWidget(summary_page)

    @staticmethod
    def _create_text_page(
        title,
        guidance,
        input_widget,
        placeholder,
    ):
        page = QWidget()
        layout = QVBoxLayout(page)

        title_label = QLabel(f"<h2>{title}</h2>")

        guidance_label = QLabel(guidance)
        guidance_label.setWordWrap(True)

        input_widget.setPlaceholderText(placeholder)

        layout.addWidget(title_label)
        layout.addWidget(guidance_label)
        layout.addSpacing(10)
        layout.addWidget(input_widget, 1)

        return page

    def previous_page(self):
        if self.current_page_index <= 0:
            return

        self.current_page_index -= 1
        self.pages.setCurrentIndex(
            self.current_page_index
        )

        self._update_navigation()

    def next_page(self):
        if not self._current_page_is_valid():
            return

        last_page_index = len(self.PAGE_TITLES) - 1

        if self.current_page_index == last_page_index:
            self.accept()
            return

        self.current_page_index += 1

        if self.current_page_index == last_page_index:
            self._update_summary()

        self.pages.setCurrentIndex(
            self.current_page_index
        )

        self._update_navigation()

    def _current_page_is_valid(self):
        if self.current_page_index == 0:
            if not self.target_readiness().strip():
                self.target_readiness_input.setFocus()
                return False

        return True

    def _update_navigation(self):
        page_number = self.current_page_index + 1
        total_pages = len(self.PAGE_TITLES)
        page_title = self.PAGE_TITLES[
            self.current_page_index
        ]

        self.stage_label.setText(
            f"<b>Readiness Analysis</b><br>"
            f"{page_title}<br>"
            f"Stage {page_number} of {total_pages}"
        )

        self.progress_bar.setValue(page_number)

        self.back_button.setEnabled(
            self.current_page_index > 0
        )

        if self.current_page_index == total_pages - 1:
            self.next_button.setText("Create Exercise")
        else:
            self.next_button.setText("Continue")

    def _update_summary(self):
        sections = [
            (
                "Target Readiness",
                self.target_readiness(),
            ),
            (
                "Operational Requirement",
                self.operational_requirement(),
            ),
            (
                "Current Readiness",
                self.current_readiness(),
            ),
            (
                "Required Standard",
                self.required_standard(),
            ),
            (
                "Readiness Gap",
                self.readiness_gap(),
            ),
            (
                "Training Audience",
                self.training_audience(),
            ),
            (
                "Learning Opportunities",
                self.learning_opportunities(),
            ),
        ]

        summary_parts = []

        for heading, value in sections:
            displayed_value = value or "Not yet defined"

            summary_parts.append(
                f"<b>{heading}</b><br>"
                f"{displayed_value}"
            )

        self.summary_label.setText(
            "<br><br>".join(summary_parts)
        )

    def target_readiness(self):
        return (
            self.target_readiness_input
            .toPlainText()
            .strip()
        )

    def operational_requirement(self):
        return (
            self.operational_requirement_input
            .toPlainText()
            .strip()
        )

    def current_readiness(self):
        return (
            self.current_readiness_input
            .toPlainText()
            .strip()
        )

    def required_standard(self):
        return (
            self.required_standard_input
            .toPlainText()
            .strip()
        )

    def readiness_gap(self):
        return (
            self.readiness_gap_input
            .toPlainText()
            .strip()
        )

    def training_audience(self):
        return (
            self.training_audience_input
            .toPlainText()
            .strip()
        )

    def learning_opportunities(self):
        return (
            self.learning_opportunities_input
            .toPlainText()
            .strip()
        )