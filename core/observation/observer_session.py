from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from core.observation.observation import (
    Observation,
    ObservationType,
)


@dataclass
class ObserverSession:
    """
    Represents an observer's working context during an exercise.

    The session identifies who is observing, what they are currently
    observing, and where they are positioned. It does not contain
    assessment or readiness decisions.
    """

    session_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    observer_name: str = ""
    observer_role: str = ""

    started_at: str = ""
    ended_at: str = ""

    current_inject_number: int | None = None
    current_activity_id: str = ""

    current_objective_titles: list[str] = field(
        default_factory=list
    )

    grid_reference: str = ""

    latitude: float | None = None
    longitude: float | None = None

    location_description: str = ""

    def start(self):
        if not self.observer_name.strip():
            raise ValueError(
                "An observer name is required to start "
                "an observer session."
            )

        if not self.started_at:
            self.started_at = datetime.now().isoformat(
                timespec="seconds"
            )

    def end(self):
        if not self.started_at:
            raise ValueError(
                "The observer session has not been started."
            )

        if not self.ended_at:
            self.ended_at = datetime.now().isoformat(
                timespec="seconds"
            )

    def set_current_inject(
    self,
    inject_number: int | None,
    ):
        self.current_inject_number = inject_number
    
    def set_current_activity(
        self,
        activity_id: str,
    ):
        self.current_activity_id = activity_id.strip()

    def add_current_objective(
        self,
        objective_title: str,
    ):
        objective_title = objective_title.strip()

        if (
            objective_title
            and objective_title
            not in self.current_objective_titles
        ):
            self.current_objective_titles.append(
                objective_title
            )

    def clear_current_objectives(self):
        self.current_objective_titles.clear()

    def set_grid_location(
        self,
        grid_reference: str,
        description: str = "",
    ):
        self.grid_reference = grid_reference.strip()

        if description:
            self.location_description = description.strip()
    def capture_observation(
        self,
        title: str,
        description: str,
        observation_type: ObservationType = (
            ObservationType.OBSERVATION
        ),
        exercise_time: str = "",
    ) -> Observation:
        if not self.started_at:
            raise ValueError(
                "The observer session must be started "
                "before recording observations."
            )

        if self.ended_at:
            raise ValueError(
                "Observations cannot be recorded after "
                "the observer session has ended."
            )

        if not description.strip():
            raise ValueError(
                "An observation must describe what "
                "was observed."
            )

        observation = Observation(
            exercise_time=exercise_time,
            observer_name=self.observer_name,
            observer_role=self.observer_role,
            observation_type=observation_type,
            title=title.strip(),
            description=description.strip(),
            related_inject_number=(
                self.current_inject_number
            ),
            related_activity_id=(
                self.current_activity_id
            ),
            related_objective_titles=list(
                self.current_objective_titles
            ),
            grid_reference=self.grid_reference,
            latitude=self.latitude,
            longitude=self.longitude,
            location_description=(
                self.location_description
            ),
        )

        observation.record(
            observer_name=self.observer_name,
            observer_role=self.observer_role,
        )

        return observation

    def set_coordinates(
        self,
        latitude: float,
        longitude: float,
        description: str = "",
    ):
        if not -90 <= latitude <= 90:
            raise ValueError(
                "Latitude must be between -90 and 90."
            )

        if not -180 <= longitude <= 180:
            raise ValueError(
                "Longitude must be between -180 and 180."
            )

        self.latitude = latitude
        self.longitude = longitude

        if description:
            self.location_description = description.strip()

    def clear_location(self):
        self.grid_reference = ""
        self.latitude = None
        self.longitude = None
        self.location_description = ""
