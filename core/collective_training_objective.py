from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class EvidenceRequirement:
    """
    Describes evidence that could support assessment of
    collective performance.
    """

    description: str
    evidence_type: str = ""
    notes: str = ""

    id: str = field(
        default_factory=lambda: str(uuid4())
    )


@dataclass
class PerformanceMetric:
    """
    An observable or measurable indicator of performance.
    """

    description: str
    category: str = ""
    evidence_requirements: list[EvidenceRequirement] = field(
        default_factory=list
    )

    id: str = field(
        default_factory=lambda: str(uuid4())
    )


@dataclass
class SuccessFactor:
    """
    Performance that indicates the collective is succeeding.
    """

    description: str
    metrics: list[PerformanceMetric] = field(
        default_factory=list
    )

    id: str = field(
        default_factory=lambda: str(uuid4())
    )


@dataclass
class CriticalError:
    """
    A failure or action significant enough to undermine
    successful collective performance.
    """

    description: str
    metrics: list[PerformanceMetric] = field(
        default_factory=list
    )

    id: str = field(
        default_factory=lambda: str(uuid4())
    )


@dataclass
class CollectiveTask:
    """
    A task that contributes to achievement of the collective
    training objective.
    """

    title: str
    description: str = ""

    success_factors: list[SuccessFactor] = field(
        default_factory=list
    )

    critical_errors: list[CriticalError] = field(
        default_factory=list
    )

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    def __str__(self):
        return self.title


@dataclass
class CollectiveTrainingObjective:
    """
    A measurable outcome that a collective must achieve.

    Individual contributions may enable the outcome, but the
    objective itself describes collective performance.
    """

    title: str

    training_audience: str = ""
    required_outcome: str = ""
    conditions: str = ""

    challenge_level: int | None = None

    collective_tasks: list[CollectiveTask] = field(
        default_factory=list
    )

    contributing_functions: list[str] = field(
        default_factory=list
    )

    individual_contributions: list[str] = field(
        default_factory=list
    )

    evidence_requirements: list[EvidenceRequirement] = field(
        default_factory=list
    )

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    def __str__(self):
        return self.title

    def has_collective_structure(self) -> bool:
        """
        Basic structural indication that the objective describes
        more than isolated individual performance.
        """

        return bool(
            self.training_audience.strip()
            and self.required_outcome.strip()
            and self.collective_tasks
        )

    def collective_test_reasons(self) -> list[str]:
        """
        Returns advisory reasons explaining weaknesses in the
        current collective objective design.

        This is guidance, not an assessment decision.
        """

        reasons = []

        if not self.training_audience.strip():
            reasons.append(
                "No collective training audience has been identified."
            )

        if not self.required_outcome.strip():
            reasons.append(
                "No required collective outcome has been defined."
            )

        if not self.collective_tasks:
            reasons.append(
                "No collective tasks have been defined."
            )

        if (
            self.individual_contributions
            and not self.collective_tasks
        ):
            reasons.append(
                "Individual contributions are present without "
                "defined collective tasks."
            )

        if (
            self.collective_tasks
            and not any(
                task.success_factors
                for task in self.collective_tasks
            )
        ):
            reasons.append(
                "Collective tasks have no success factors."
            )

        return reasons

    def passes_collective_structure_test(self) -> bool:
        return not self.collective_test_reasons()
    def success_factors(self) -> list[SuccessFactor]:
        """
        Return all success factors across all collective tasks.
        """

        factors = []

        for task in self.collective_tasks:
            factors.extend(
                task.success_factors
            )

        return factors

    def success_factors_without_metrics(
        self,
    ) -> list[SuccessFactor]:
        """
        Return success factors for which no observable or
        measurable performance metric has been defined.
        """

        return [
            factor
            for factor in self.success_factors()
            if not factor.metrics
        ]

    def metrics_without_evidence_requirements(
        self,
    ) -> list[PerformanceMetric]:
        """
        Return performance metrics that currently have no
        defined evidence requirement.
        """

        gaps = []

        for factor in self.success_factors():
            for metric in factor.metrics:
                if not metric.evidence_requirements:
                    gaps.append(metric)

        return gaps

    def has_evidence_coverage(self) -> bool:
        """
        True when every success factor has at least one metric
        and every metric has at least one evidence requirement.
        """

        factors = self.success_factors()

        if not factors:
            return False

        return bool(
            not self.success_factors_without_metrics()
            and not self.metrics_without_evidence_requirements()
        )
    def critical_errors(self) -> list[CriticalError]:
        """
        Return all critical errors across all collective tasks.
        """

        errors = []

        for task in self.collective_tasks:
            errors.extend(
                task.critical_errors
            )

        return errors

    def critical_errors_without_metrics(
        self,
    ) -> list[CriticalError]:
        """
        Return critical errors for which no observable or
        measurable performance metric has been defined.
        """

        return [
            error
            for error in self.critical_errors()
            if not error.metrics
        ]

    def critical_error_metrics_without_evidence_requirements(
        self,
    ) -> list[PerformanceMetric]:
        """
        Return critical-error metrics that currently have no
        defined evidence requirement.
        """

        gaps = []

        for error in self.critical_errors():
            for metric in error.metrics:
                if not metric.evidence_requirements:
                    gaps.append(metric)

        return gaps

    def has_critical_error_coverage(self) -> bool:
        """
        True when every defined critical error has at least one
        metric and every metric has an evidence requirement.

        A CTO with no defined critical errors is not considered
        incomplete solely because none have been identified.
        """

        errors = self.critical_errors()

        if not errors:
            return True

        return bool(
            not self.critical_errors_without_metrics()
            and not (
                self
                .critical_error_metrics_without_evidence_requirements()
            )
        )
