from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.observation.observer_session import ObserverSession
from core.observation.observation import ObservationType
from core.inject import InjectStatus


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
        self.project = None
        self.assurance_tasking = None

        self._build_ui()

        self.record_button.clicked.connect(
            self._record_observation
        )

        self.start_session_button.clicked.connect(
            self._start_observer_session
        )
        self.update_location_button.clicked.connect(
            self._update_observer_location
        )
    def _build_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        page = QWidget()
        page.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.MinimumExpanding,
        )

        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )
        main_layout.setSpacing(12)

        # -------------------------------------------------
        # Header
        # -------------------------------------------------

        header_layout = QHBoxLayout()

        title_label = QLabel(
            "OBSERVER MODE"
        )
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

        header_layout.addWidget(
            title_label
        )
        header_layout.addStretch()
        header_layout.addWidget(
            self.exercise_time_label
        )

        main_layout.addLayout(
            header_layout
        )

        # -------------------------------------------------
        # Observer
        # -------------------------------------------------

        self.observer_label = QLabel(
            "No observer session active"
        )
        self.observer_label.setStyleSheet(
            "font-weight: bold;"
        )

        main_layout.addWidget(
            self.observer_label
        )

        # -------------------------------------------------
        # Observer session
        # -------------------------------------------------

        session_frame = QFrame()
        session_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        session_layout = QHBoxLayout(
            session_frame
        )

        self.observer_name_input = QLineEdit()
        self.observer_name_input.setPlaceholderText(
            "Observer name"
        )

        self.observer_role_input = QLineEdit()
        self.observer_role_input.setPlaceholderText(
            "Observer role"
        )

        self.start_session_button = QPushButton(
            "START OBSERVER SESSION"
        )

        session_layout.addWidget(
            self.observer_name_input
        )
        session_layout.addWidget(
            self.observer_role_input
        )
        session_layout.addWidget(
            self.start_session_button
        )

        main_layout.addWidget(
            session_frame
        )

        # -------------------------------------------------
        # Current activity
        # -------------------------------------------------

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
        self.objective_label.setWordWrap(
            True
        )

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

        # -------------------------------------------------
        # Assurance tasking
        # -------------------------------------------------

        assurance_frame = QFrame()
        assurance_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )
        assurance_frame.setMinimumHeight(
            210
        )
        assurance_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )
        assurance_layout = QVBoxLayout(
            assurance_frame
        )

        assurance_heading = QLabel(
            "ASSURANCE TASKING"
        )
        assurance_heading.setStyleSheet(
            "font-weight: bold;"
        )

        self.assurance_status_label = QLabel(
            "No assured observer tasking for the current MEL/MIL item."
        )
        self.assurance_status_label.setWordWrap(True)
        self.assurance_status_label.setMinimumHeight(
            24
        )

        self.success_factor_label = QLabel(
            "Success Factor: -"
        )
        self.success_factor_label.setWordWrap(True)
        self.success_factor_label.setMinimumHeight(
            24
        )

        self.observable_metric_label = QLabel(
            "Observable Metric: -"
        )
        self.observable_metric_label.setWordWrap(True)
        self.observable_metric_label.setMinimumHeight(
            24
        )

        self.evidence_requirement_label = QLabel(
            "Evidence Requirement: -"
        )
        self.evidence_requirement_label.setWordWrap(True)
        self.evidence_requirement_label.setMinimumHeight(
            24
        )

        assurance_note = QLabel(
            "Read-only assurance guidance. Record only what you actually "
            "observe; Observer Mode does not make the assessment decision."
        )
        assurance_note.setWordWrap(True)
        assurance_note.setStyleSheet(
            "font-style: italic;"
        )

        for widget in (
            assurance_heading,
            self.assurance_status_label,
            self.success_factor_label,
            self.observable_metric_label,
            self.evidence_requirement_label,
            assurance_note,
        ):
            assurance_layout.addWidget(widget)

        main_layout.addWidget(
            assurance_frame
        )

        # -------------------------------------------------
        # Location
        # -------------------------------------------------

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
        self.location_label.setWordWrap(
            True
        )

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
        # -------------------------------------------------
        # Update observer location
        # -------------------------------------------------

        location_input_frame = QFrame()
        location_input_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        location_input_layout = QHBoxLayout(
            location_input_frame
        )

        self.grid_input = QLineEdit()
        self.grid_input.setPlaceholderText(
            "Grid reference"
        )

        self.latitude_input = QLineEdit()
        self.latitude_input.setPlaceholderText(
            "Latitude"
        )

        self.longitude_input = QLineEdit()
        self.longitude_input.setPlaceholderText(
            "Longitude"
        )

        self.location_description_input = QLineEdit()
        self.location_description_input.setPlaceholderText(
            "Location description"
        )

        self.update_location_button = QPushButton(
            "UPDATE LOCATION"
        )

        location_input_layout.addWidget(
            self.grid_input
        )

        location_input_layout.addWidget(
            self.latitude_input
        )

        location_input_layout.addWidget(
            self.longitude_input
        )

        location_input_layout.addWidget(
            self.location_description_input
        )

        location_input_layout.addWidget(
            self.update_location_button
        )

        main_layout.addWidget(
            location_input_frame
        )
        # -------------------------------------------------
        # Observation capture
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Observation type
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Record button
        # -------------------------------------------------

        self.record_button = QPushButton(
            "RECORD OBSERVATION"
        )
        self.record_button.setMinimumHeight(
            40
        )

        main_layout.addWidget(
            self.record_button
        )

        # -------------------------------------------------
        # Recent observations
        # -------------------------------------------------

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

        main_layout.setSizeConstraint(
            QVBoxLayout.SizeConstraint.SetMinimumSize
        )

        scroll_area.setWidget(page)
        outer_layout.addWidget(scroll_area)

    def _update_observer_location(self):
        if self.session is None:
            return

        grid_reference = (
            self.grid_input
            .text()
            .strip()
        )

        latitude_text = (
            self.latitude_input
            .text()
            .strip()
        )

        longitude_text = (
            self.longitude_input
            .text()
            .strip()
        )

        location_description = (
            self.location_description_input
            .text()
            .strip()
        )

        if latitude_text and longitude_text:
            try:
                latitude = float(latitude_text)
                longitude = float(longitude_text)
            except ValueError:
                return

            self.session.set_coordinates(
                latitude,
                longitude,
                location_description,
            )

        elif grid_reference:
            self.session.set_grid_location(
                grid_reference,
                location_description,
            )

        else:
            return

        self.refresh_session_view()

    def set_project(self, project):
        self.project = project
        self.refresh_assurance_tasking()

    def _find_promotion_for_inject(
        self,
        inject_number,
    ):
        if self.project is None:
            return None

        wanted = str(inject_number)

        for promotion in getattr(
            self.project,
            "mel_mil_promotions",
            [],
        ):
            if str(promotion.inject_number) == wanted:
                return promotion

        return None

    def _find_cto(self, cto_id: str):
        if self.project is None:
            return None

        for cto in getattr(
            self.project,
            "collective_training_objectives",
            [],
        ):
            if cto.id == cto_id:
                return cto

        return None

    @staticmethod
    def _find_success_factor(cto, success_factor_id: str):
        if cto is None:
            return None

        for task in cto.collective_tasks:
            for factor in task.success_factors:
                if factor.id == success_factor_id:
                    return factor

        return None

    @staticmethod
    def _metric_texts(cto, metric_ids):
        if cto is None:
            return []

        wanted = set(metric_ids)
        return [
            metric.description
            for task in cto.collective_tasks
            for factor in task.success_factors
            for metric in factor.metrics
            if metric.id in wanted
        ]

    @staticmethod
    def _evidence_texts(cto, evidence_ids):
        if cto is None:
            return []

        wanted = set(evidence_ids)
        results = []

        for task in cto.collective_tasks:
            for factor in task.success_factors:
                for metric in factor.metrics:
                    for requirement in metric.evidence_requirements:
                        if requirement.id not in wanted:
                            continue

                        value = requirement.description
                        if requirement.evidence_type:
                            value += f" [{requirement.evidence_type}]"
                        if requirement.notes:
                            value += f" — {requirement.notes}"
                        results.append(value)

        return results

    def refresh_assurance_tasking(self):
        if not hasattr(self, "assurance_status_label"):
            return

        self.assurance_tasking = None
        self.assurance_status_label.setText(
            "No assured observer tasking for the current MEL/MIL item."
        )
        self.success_factor_label.setText("Success Factor: -")
        self.observable_metric_label.setText("Observable Metric: -")
        self.evidence_requirement_label.setText(
            "Evidence Requirement: -"
        )

        if self.project is None or self.session is None:
            return

        inject_number = self.session.current_inject_number
        if inject_number is None:
            return

        promotion = self._find_promotion_for_inject(
            inject_number
        )

        if promotion is None:
            self.assurance_status_label.setText(
                f"No assured design promotion lineage was found for "
                f"MEL/MIL #{inject_number}."
            )
            return

        inject = next(
            (
                item
                for item in getattr(
                    self.project,
                    "injects",
                    [],
                )
                if str(item.number) == str(inject_number)
            ),
            None,
        )

        if (
            inject is None
            or inject.status not in (
                InjectStatus.READY,
                InjectStatus.ISSUED,
                InjectStatus.RESPONSE_RECEIVED,
                InjectStatus.CLOSED,
            )
        ):
            self.assurance_status_label.setText(
                "Assurance lineage exists, but this MEL/MIL item is not "
                "READY FOR EXCON. Observer tasking is withheld."
            )
            return

        cto = self._find_cto(promotion.cto_id)
        factor = self._find_success_factor(
            cto,
            promotion.success_factor_id,
        )
        metrics = self._metric_texts(
            cto,
            promotion.metric_ids,
        )
        evidence = self._evidence_texts(
            cto,
            promotion.evidence_requirement_ids,
        )

        self.assurance_tasking = {
            "cto_id": promotion.cto_id,
            "success_factor_id": promotion.success_factor_id,
            "metric_ids": list(promotion.metric_ids),
            "evidence_requirement_ids": list(
                promotion.evidence_requirement_ids
            ),
        }

        self.assurance_status_label.setText(
            f"Assured observer tasking for MEL/MIL #{inject_number}"
        )
        self.success_factor_label.setText(
            "Success Factor: "
            + (
                factor.description
                if factor is not None
                else "Not found — review lineage"
            )
        )
        self.observable_metric_label.setText(
            "Observable Metric: "
            + (
                " | ".join(metrics)
                if metrics
                else "Not found — review lineage"
            )
        )
        self.evidence_requirement_label.setText(
            "Evidence Requirement: "
            + (
                " | ".join(evidence)
                if evidence
                else "Not found — review lineage"
            )
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
            self.refresh_assurance_tasking()
            return

        observer_text = (
            self.session.observer_name
        )

        if self.session.observer_role:
            observer_text += (
                f" - {self.session.observer_role}"
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

        if self.session.current_objective_titles:
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
            and self.session.longitude is not None
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

        self.refresh_assurance_tasking()

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

    def _start_observer_session(self):
        observer_name = (
            self.observer_name_input
            .text()
            .strip()
        )

        observer_role = (
            self.observer_role_input
            .text()
            .strip()
        )

        if not observer_name:
            return

        session = ObserverSession(
            observer_name=observer_name,
            observer_role=observer_role,
        )

        session.start()

        self.set_session(
            session
        )

        self.observer_name_input.setEnabled(
            False
        )

        self.observer_role_input.setEnabled(
            False
        )

        self.start_session_button.setEnabled(
            False
        )
