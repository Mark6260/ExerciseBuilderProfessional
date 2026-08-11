from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QRadioButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.observation.observer_session import ObserverSession
from core.observation.observation import ObservationType

class ObserverPanel(QWidget):
    """
    Observer Mode working panel.

    Displays the current observer session and provides
    the working area for observation capture.
    """
    observation_recorded = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.session: ObserverSession | None = None

        self._build_ui()
        self.record_button.clicked.connect(
            self._record_observation
        )
    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Header
        header_layout = QHBoxLayout()

        title_label = QLabel("OBSERVER MODE")
        title_label.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        self.exercise_time_label = QLabel(
            "EX TIME  --:--"
        )
        self.exercise_time_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(
            self.exercise_time_label
        )

        main_layout.addLayout(header_layout)

        # Observer
        self.observer_label = QLabel(
            "No observer session active"
        )
        self.observer_label.setStyleSheet(
            "font-weight: bold;"
        )

        main_layout.addWidget(
            self.observer_label
        )

        # Current activity
        activity_frame = QFrame()
        activity_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        activity_layout = QVBoxLayout(
            activity_frame
        )

        activity_heading = QLabel(
            "CURRENT ACTIVITY"
        )
        activity_heading.setStyleSheet(
            "font-weight: bold;"
        )

        self.inject_label = QLabel(
            "Inject: -"
        )

        self.activity_label = QLabel(
            "Activity: -"
        )

        self.objective_label = QLabel(
            "Objective: -"
        )
        self.objective_label.setWordWrap(True)

        activity_layout.addWidget(
            activity_heading
        )
        activity_layout.addWidget(
            self.inject_label
        )
        activity_layout.addWidget(
            self.activity_label
        )
        activity_layout.addWidget(
            self.objective_label
        )

        main_layout.addWidget(
            activity_frame
        )

        # Location
        location_frame = QFrame()
        location_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        location_layout = QVBoxLayout(
            location_frame
        )

        location_heading = QLabel(
            "LOCATION"
        )
        location_heading.setStyleSheet(
            "font-weight: bold;"
        )

        self.grid_label = QLabel(
            "Grid: -"
        )

        self.coordinates_label = QLabel(
            "Coordinates: -"
        )

        self.location_label = QLabel(
            "Location: -"
        )
        self.location_label.setWordWrap(True)

        location_layout.addWidget(
            location_heading
        )
        location_layout.addWidget(
            self.grid_label
        )
        location_layout.addWidget(
            self.coordinates_label
        )
        location_layout.addWidget(
            self.location_label
        )

        main_layout.addWidget(
            location_frame
        )

        # Observation capture
        observation_heading = QLabel(
            "WHAT DID YOU OBSERVE?"
        )
        observation_heading.setStyleSheet(
            "font-weight: bold;"
        )

        main_layout.addWidget(
            observation_heading
        )

        self.observation_text = QTextEdit()
        self.observation_text.setPlaceholderText(
            "Record what you saw, heard, or "
            "otherwise directly observed..."
        )

        main_layout.addWidget(
            self.observation_text
        )

        # Observation type
        type_layout = QHBoxLayout()

        self.effective_practice_radio = (
            QRadioButton(
                "Effective Practice"
            )
        )

        self.observation_radio = (
            QRadioButton(
                "Observation"
            )
        )

        self.concern_radio = (
            QRadioButton(
                "Concern"
            )
        )

        self.evidence_gap_radio = (
            QRadioButton(
                "Evidence Gap"
            )
        )

        self.observation_radio.setChecked(
            True
        )

        self.observation_type_group = (
            QButtonGroup(self)
        )

        for button in (
            self.effective_practice_radio,
            self.observation_radio,
            self.concern_radio,
            self.evidence_gap_radio,
        ):
            self.observation_type_group.addButton(
                button
            )
            type_layout.addWidget(
                button
            )

        main_layout.addLayout(
            type_layout
        )

        # Record button
        self.record_button = QPushButton(
            "RECORD OBSERVATION"
        )
        self.record_button.setMinimumHeight(
            40
        )

        main_layout.addWidget(
            self.record_button
        )

        # Recent observations
        recent_heading = QLabel(
            "RECENT OBSERVATIONS"
        )
        recent_heading.setStyleSheet(
            "font-weight: bold;"
        )

        main_layout.addWidget(
            recent_heading
        )

        self.recent_observations_list = (
            QListWidget()
        )
        self.recent_observations_list.setMinimumHeight(
            120
        )

        main_layout.addWidget(
            self.recent_observations_list
        )

    def set_session(
        self,
        session: ObserverSession,
    ):
        self.session = session
        self.refresh_session_view()

    def refresh_session_view(self):
        if self.session is None:
            self.observer_label.setText(
                "No observer session active"
            )
            self.inject_label.setText(
                "Inject: -"
            )
            self.activity_label.setText(
                "Activity: -"
            )
            self.objective_label.setText(
                "Objective: -"
            )
            self.grid_label.setText(
                "Grid: -"
            )
            self.coordinates_label.setText(
                "Coordinates: -"
            )
            self.location_label.setText(
                "Location: -"
            )
            return

        observer_text = (
            self.session.observer_name
        )

        if self.session.observer_role:
            observer_text += (
                f" - "
                f"{self.session.observer_role}"
            )

        self.observer_label.setText(
            observer_text
        )

        inject_text = (
            str(
                self.session.current_inject_number
            )
            if (
                self.session.current_inject_number
                is not None
            )
            else "-"
        )

        self.inject_label.setText(
            f"Inject: {inject_text}"
        )

        activity_text = (
            self.session.current_activity_id
            or "-"
        )

        self.activity_label.setText(
            f"Activity: {activity_text}"
        )

        if (
            self.session.current_objective_titles
        ):
            objective_text = " | ".join(
                self.session.current_objective_titles
            )
        else:
            objective_text = "-"

        self.objective_label.setText(
            f"Objective: {objective_text}"
        )

        self.grid_label.setText(
            "Grid: "
            f"{self.session.grid_reference or '-'}"
        )

        if (
            self.session.latitude is not None
            and self.session.longitude
            is not None
        ):
            coordinates = (
                f"{self.session.latitude:.6f}, "
                f"{self.session.longitude:.6f}"
            )
        else:
            coordinates = "-"

        self.coordinates_label.setText(
            f"Coordinates: {coordinates}"
        )

        self.location_label.setText(
            "Location: "
            f"{self.session.location_description or '-'}"
        )
    def _selected_observation_type(
        self,
    ) -> ObservationType:
        if self.effective_practice_radio.isChecked():
            return ObservationType.EFFECTIVE_PRACTICE

        if self.concern_radio.isChecked():
            return ObservationType.CONCERN

        if self.evidence_gap_radio.isChecked():
            return ObservationType.EVIDENCE_GAP

        return ObservationType.OBSERVATION


    def _record_observation(self):
        if self.session is None:
            return

        description = (
            self.observation_text
            .toPlainText()
            .strip()
        )

        if not description:
            return

        observation_type = (
            self._selected_observation_type()
        )

        title = description

        if len(title) > 60:
            title = (
                title[:57].rstrip()
                + "..."
            )

        observation = (
            self.session.capture_observation(
                title=title,
                description=description,
                observation_type=observation_type,
            )
        )

        self.observation_recorded.emit(
            observation
        )

        recent_text = (
            f"{observation.observation_type.value}"
            f" - {observation.title}"
        )

        self.recent_observations_list.insertItem(
            0,
            recent_text,
        )

        self.observation_text.clear()

        self.observation_radio.setChecked(
            True
        )
