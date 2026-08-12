from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ObservationReviewPanel(QWidget):
    evidence_admitted = Signal(object)
    """
    Workspace for reviewing recorded observations.

    Review is deliberately separated from live observer capture.
    Assessment and readiness decisions do not belong here.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.project = None

        self._build_ui()
        self.observation_list.currentRowChanged.connect(
            self._show_selected_observation
        )
        self.mark_reviewed_button.clicked.connect(
            self._mark_selected_reviewed
        )

        self.admit_evidence_button.clicked.connect(
            self._admit_selected_as_evidence
        )
    def _mark_selected_reviewed(self):
        observation = self._selected_observation()

        if observation is None:
            return

        reviewer_name = "Chief Observer"

        observation.mark_reviewed(
            reviewed_by=reviewer_name
        )

        self.status_label.setText(
            f"Status: {observation.status.value}"
        )

        self.admit_evidence_button.setEnabled(
            True
        )

        self.refresh_observations()

        row = self.project.observations.index(
            observation
        )

        self.observation_list.setCurrentRow(
            row
        )
    def _build_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # -------------------------------------------------
        # Recorded observations
        # -------------------------------------------------

        left_frame = QFrame()
        left_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        left_layout = QVBoxLayout(left_frame)

        heading = QLabel(
            "RECORDED OBSERVATIONS"
        )
        heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.observation_list = QListWidget()

        left_layout.addWidget(heading)
        left_layout.addWidget(
            self.observation_list
        )

        # -------------------------------------------------
        # Review detail
        # -------------------------------------------------

        right_frame = QFrame()
        right_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        right_layout = QVBoxLayout(right_frame)

        review_heading = QLabel(
            "OBSERVATION REVIEW"
        )
        review_heading.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.status_label = QLabel(
            "Status: -"
        )

        self.observer_label = QLabel(
            "Observer: -"
        )

        self.exercise_time_label = QLabel(
            "Exercise Time: -"
        )

        self.inject_label = QLabel(
            "Inject: -"
        )

        self.objective_label = QLabel(
            "Objective: -"
        )
        self.objective_label.setWordWrap(True)

        self.location_label = QLabel(
            "Location: -"
        )
        self.location_label.setWordWrap(True)
        description_heading = QLabel(
            "WHAT WAS OBSERVED"
        )
        description_heading.setStyleSheet(
            "font-weight: bold;"
        )

        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)

        review_heading_2 = QLabel(
            "REVIEW"
        )
        review_heading_2.setStyleSheet(
            "font-weight: bold;"
        )

        self.review_notes = QTextEdit()
        self.review_notes.setPlaceholderText(
            "Record review notes..."
        )

        button_layout = QHBoxLayout()

        self.mark_reviewed_button = QPushButton(
            "MARK REVIEWED"
        )

        self.admit_evidence_button = QPushButton(
            "ADMIT AS EVIDENCE"
        )

        self.admit_evidence_button.setEnabled(
            False
        )

        button_layout.addWidget(
            self.mark_reviewed_button
        )
        button_layout.addWidget(
            self.admit_evidence_button
        )

        right_layout.addWidget(review_heading)
        right_layout.addWidget(self.status_label)
        right_layout.addWidget(self.observer_label)
        right_layout.addWidget(
            self.exercise_time_label
        )
        right_layout.addWidget(self.inject_label)
        right_layout.addWidget(
            self.objective_label
        )
        right_layout.addWidget(
            self.location_label
        )
        right_layout.addWidget(
            description_heading
        )
        right_layout.addWidget(
            self.description_text
        )
        right_layout.addWidget(
            review_heading_2
        )
        right_layout.addWidget(
            self.review_notes
        )
        right_layout.addLayout(button_layout)

        main_layout.addWidget(left_frame, 4)
        main_layout.addWidget(right_frame, 6)
    def _selected_observation(self):
        if self.project is None:
            return None

        row = self.observation_list.currentRow()

        if row < 0:
            return None

        if row >= len(self.project.observations):
            return None

        return self.project.observations[row]

    def _show_selected_observation(
        self,
        row: int,
    ):
        observation = self._selected_observation()

        if observation is None:
            self.status_label.setText(
                "Status: "-""
            )
            self.observer_label.setText(
                "Observer: "-""
            )
            self.exercise_time_label.setText(
                f"Exercise Time: {observation.exercise_time or '-'}"
            )
            self.inject_label.setText(
                "Inject: "-""
            )
            self.objective_label.setText(
                "Objective: "-""
            )
            self.location_label.setText(
                "Location: "-""
            )
            self.description_text.clear()
            self.admit_evidence_button.setEnabled(
                False
            )
            return

        self.status_label.setText(
            f"Status: {observation.status.value}"
        )

        observer_text = observation.observer_name

        if observation.observer_role:
            observer_text += (
                f" - {observation.observer_role}"
            )

        self.observer_label.setText(
            f"Observer: {observer_text}"
        )

        self.exercise_time_label.setText(
            "Exercise Time: "
            + (
                observation.exercise_time
                if observation.exercise_time
                else "-"
            )
        )

        inject_text = (
            str(observation.related_inject_number)
            if observation.related_inject_number
            is not None
            else ""-""
        )

        self.inject_label.setText(
            f"Inject: {inject_text}"
        )

        if observation.related_objective_titles:
            objective_text = " | ".join(
                observation.related_objective_titles
            )
        else:
            objective_text = ""-""

        self.objective_label.setText(
            f"Objective: {objective_text}"
        )

        location_parts = []

        if observation.grid_reference:
            location_parts.append(
                f"Grid {observation.grid_reference}"
            )

        if (
            observation.latitude is not None
            and observation.longitude is not None
        ):
            location_parts.append(
                f"{observation.latitude:.6f}, "
                f"{observation.longitude:.6f}"
            )

        if observation.location_description:
            location_parts.append(
                observation.location_description
            )

        location_text = (
            " | ".join(location_parts)
            if location_parts
            else ""-""
        )

        self.location_label.setText(
            f"Location: {location_text}"
        )

        self.description_text.setPlainText(
            observation.description
        )

        self.admit_evidence_button.setEnabled(
            observation.status.value
            == "Reviewed"
        )

    def set_project(self, project):
        self.project = project
        self.refresh_observations()

    def refresh_observations(self):
        self.observation_list.clear()

        if self.project is None:
            return

        for observation in self.project.observations:
            item_text = (
                f"{observation.observation_type.value}"
                f" - {observation.title}"
            )

            self.observation_list.addItem(
                item_text
            )
    def _admit_selected_as_evidence(self):
        observation = self._selected_observation()

        if observation is None:
            return

        evidence = observation.to_evidence_record()

        self.evidence_admitted.emit(
            evidence
        )

        self.admit_evidence_button.setEnabled(
            False
        )

        self.status_label.setText(
            f"Status: {observation.status.value}"
        )
