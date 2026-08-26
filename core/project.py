import json
from pathlib import Path

from core import assessment
from core.doctrine import DoctrineReference
from core.inject import Inject, InjectStatus
from core.objective import ExerciseObjective
from core.exercise_design_opportunity import ExerciseDesignOpportunity
from core.candidate_exercise_activity import CandidateExerciseActivity
from core.candidate_mel_mil_activity import CandidateMelMilActivity
from core.mel_mil_promotion import MelMilPromotion
from core.collective_training_objective import (
    CollectiveTrainingObjective,
    CollectiveTask,
    SuccessFactor,
    CriticalError,
    PerformanceMetric,
    EvidenceRequirement,
)

from core.design_trace import (
    DesignTraceEventType,
    DesignTraceRecord,
)
from core.readiness import OperationalRequirement
from core.readiness.readiness import OperationalReadiness
from core.readiness.readiness_gap import ReadinessGap
from core.apprentice import ApprenticeNotebook
from core.evidence import EvidenceRecord, EvidenceType
from uuid import uuid4
from core.assessment import AssessmentRecord, AssessmentOutcome
from core.improvement.finding import Finding, FindingType
from core.improvement.recommendation import (
    Recommendation,
    RecommendationDisposition,
    RecommendationType,
)
from core.preparedness import (
    ConfidenceAssessment,
    ConfidenceStage,
    DemonstratedStrength,
    LearningEvent,
    LearningOpportunityState,
    PreparednessScope,
)
from core.improvement.action import (
    ActionPriority,
    ActionStatus,
    ImprovementAction,
)
from core.improvement.verification import (
    ImprovementVerification,
    VerificationOutcome,
)
from core.improvement.training_opportunity import (
    TrainingOpportunity,
    TrainingOpportunityStatus,
)
from core.readiness.readiness_decision import (
    AssessmentExceptionReason,
    ReadinessDecision,
    ReadinessDecisionOutcome,
)
from core.opportunity.candidate_opportunity import (
    CandidateOpportunity,
    CandidateStatus,
    OpportunitySourceType,
)
from core.opportunity.discovery_requirement import (
    DiscoveryRequirement,
)
from core.opportunity.planned_activity import (
    PlannedActivity,
    PlannedActivitySourceType,
)
from core.opportunity.planning_source import (
    PlanningSource,
    PlanningSourceStatus,
    PlanningSourceType,
)
from core.observation.observation import (
    Observation,
    ObservationStatus,
    ObservationType,
)


class Project:
    def __init__(self, name="Untitled Project"):
        self.name = name

        self.operational_requirement = OperationalRequirement()
        self.apprentice_notebook = ApprenticeNotebook()

        self.injects: list[Inject] = []
        self.objectives: list[ExerciseObjective] = []
        self.design_trace_records: list[
            DesignTraceRecord
        ] = []
        self.exercise_design_opportunities: list[ExerciseDesignOpportunity] = []
        self.candidate_exercise_activities: list[CandidateExerciseActivity] = []
        self.candidate_mel_mil_activities: list[CandidateMelMilActivity] = []
        self.mel_mil_promotions: list[MelMilPromotion] = []
        self.collective_training_objectives: list[
            CollectiveTrainingObjective
        ] = []
        self.doctrine_references: list[DoctrineReference] = []
        self.observations: list[Observation] = []
        self.evidence_records: list[EvidenceRecord] = []
        self.assessment_records: list[AssessmentRecord] = []
        self.confidence_assessments: list[
            ConfidenceAssessment
        ] = []

        self.learning_events: list[
            LearningEvent
        ] = []

        self.demonstrated_strengths: list[
            DemonstratedStrength
        ] = []
        self.readiness_decisions: list[ReadinessDecision] = []
        self.findings: list[Finding] = []
        self.recommendations: list[Recommendation] = []
        self.improvement_actions: list[ImprovementAction] = []
        self.improvement_verifications: list[ImprovementVerification] = []
        self.training_opportunities: list[TrainingOpportunity] = []
        self.candidate_opportunities: list[CandidateOpportunity] = []
        self.discovery_requirements: list[DiscoveryRequirement] = []
        self.planning_sources: list[PlanningSource] = []
        self.planned_activities: list[PlannedActivity] = []

    def add_inject(self, inject: Inject):
        self.injects.append(inject)

    def add_objective(self, objective: ExerciseObjective):
        self.objectives.append(objective)

    def add_design_trace_record(
        self,
        record: DesignTraceRecord,
    ):
        self.design_trace_records.append(
            record
        )

    def add_exercise_design_opportunity(
        self,
        opportunity: ExerciseDesignOpportunity,
    ):
        self.exercise_design_opportunities.append(
            opportunity
        )

    def add_candidate_exercise_activity(
        self,
        activity: CandidateExerciseActivity,
    ):
        self.candidate_exercise_activities.append(
            activity
        )

    def add_candidate_mel_mil_activity(
        self,
        activity: CandidateMelMilActivity,
    ):
        self.candidate_mel_mil_activities.append(
            activity
        )

    def add_mel_mil_promotion(
        self,
        promotion: MelMilPromotion,
    ):
        self.mel_mil_promotions.append(
            promotion
        )

    def add_collective_training_objective(
        self,
        objective: CollectiveTrainingObjective,
    ):
        self.collective_training_objectives.append(
            objective
        )
    def add_doctrine_reference(
        self,
        doctrine_reference: DoctrineReference,
        ):
        self.doctrine_references.append(doctrine_reference)
    def add_observation(
        self,
        observation: Observation,
    ):
        self.observations.append(observation)

    def add_evidence(self, evidence: EvidenceRecord):
        self.evidence_records.append(evidence)
    def add_assessment(self, assessment: AssessmentRecord):
        self.assessment_records.append(assessment)
    def add_confidence_assessment(
        self,
        assessment: ConfidenceAssessment,
    ):
        self.confidence_assessments.append(
        assessment
    )

    def add_learning_event(
        self,
        learning_event: LearningEvent,
    ):
        self.learning_events.append(
            learning_event
        )

    def add_demonstrated_strength(
        self,
        strength: DemonstratedStrength,
    ):
        self.demonstrated_strengths.append(
            strength
        )   

    def add_readiness_decision(
        self,
        decision: ReadinessDecision,
    ):
        self.readiness_decisions.append(decision)

    def add_finding(self, finding: Finding):
        self.findings.append(finding)

    def add_recommendation(
        self,
        recommendation: Recommendation,
    ):
        self.recommendations.append(recommendation)

    def add_improvement_action(
        self,
        action: ImprovementAction,
    ):
        self.improvement_actions.append(action)

    def add_improvement_verification(
        self,
        verification: ImprovementVerification,
    ):
        self.improvement_verifications.append(verification)

    def add_training_opportunity(
        self,
        opportunity: TrainingOpportunity,
    ):
        self.training_opportunities.append(opportunity)

    def add_candidate_opportunity(
        self,
        candidate: CandidateOpportunity,
    ):
        self.candidate_opportunities.append(candidate)

    def add_discovery_requirement(
        self,
        requirement: DiscoveryRequirement,
    ):
        self.discovery_requirements.append(requirement)

    def add_planning_source(
        self,
        source: PlanningSource,
    ):
        self.planning_sources.append(source)

    def add_planned_activity(
        self,
        activity: PlannedActivity,
    ):
        self.planned_activities.append(activity)

    def save(self, filename):
        readiness_gap = self.operational_requirement.readiness.readiness_gap

        # Backwards compatibility:
        # Some live/legacy project states may still hold readiness_gap
        # as a simple string rather than a ReadinessGap object.
        if isinstance(readiness_gap, str):
            readiness_gap = ReadinessGap(
                shortfall=readiness_gap
            )
            
        project_data = {
        
            "name": self.name,

            "operational_requirement": {
                "title": self.operational_requirement.title,
                "description": self.operational_requirement.description,
                "sponsor": self.operational_requirement.sponsor,
                "operational_driver": (
                    self.operational_requirement.operational_driver
                ),
                "success_criteria": (
                    self.operational_requirement.success_criteria
                ),
                "doctrine_reference": (
                    self.operational_requirement.doctrine_reference
                ),

                "readiness": {
                    "current_state": (
                        self.operational_requirement.readiness.current_state
                    ),
                    "required_state": (
                        self.operational_requirement.readiness.required_state
                    ),
                    "required_standard": (
                        self.operational_requirement.readiness.required_standard
                    ),

                    "readiness_gap": {
                        "required_standard": readiness_gap.required_standard,
                        "current_state": readiness_gap.current_state,
                        "shortfall": readiness_gap.shortfall,
                        "consequence": readiness_gap.consequence,
                        "preparation_requirement": (
                            readiness_gap.preparation_requirement
                        ),
                        "rationale": readiness_gap.rationale,
                    },

                    "rationale": (
                        self.operational_requirement.readiness.rationale
                    ),
                },
            },

            "doctrine_references": [
                {
                    "title": doctrine.title,
                    "reference": doctrine.reference,
                    "version": doctrine.version,
                    "organisation": doctrine.organisation,
                    "description": doctrine.description,
                    "location": doctrine.location,
                }
                for doctrine in self.doctrine_references
            ],

            "objectives": [
                {
                    "title": objective.title,
                    "description": objective.description,
                    "success_criteria": objective.success_criteria,
                    "supporting_injects": objective.supporting_injects,
                    "achieved": objective.achieved,
                }
                for objective in self.objectives
            ],
            "mel_mil_promotions": [
                {
                    "id": promotion.id,
                    "inject_number": promotion.inject_number,
                    "candidate_mel_mil_activity_id": (
                        promotion.candidate_mel_mil_activity_id
                    ),
                    "candidate_activity_id": (
                        promotion.candidate_activity_id
                    ),
                    "design_opportunity_id": (
                        promotion.design_opportunity_id
                    ),
                    "cto_id": promotion.cto_id,
                    "collective_task_id": (
                        promotion.collective_task_id
                    ),
                    "success_factor_id": (
                        promotion.success_factor_id
                    ),
                    "metric_ids": promotion.metric_ids,
                    "evidence_requirement_ids": (
                        promotion.evidence_requirement_ids
                    ),
                }
                for promotion in self.mel_mil_promotions
            ],

            "candidate_mel_mil_activities": [
                {
                    "id": activity.id,
                    "title": activity.title,
                    "activity_type": activity.activity_type,
                    "phase": activity.phase,
                    "timing_window": activity.timing_window,
                    "event_summary": activity.event_summary,
                    "intended_effect": activity.intended_effect,
                    "control_notes": activity.control_notes,
                    "candidate_activity_id": activity.candidate_activity_id,
                    "design_opportunity_id": activity.design_opportunity_id,
                    "cto_id": activity.cto_id,
                    "collective_task_id": activity.collective_task_id,
                    "success_factor_id": activity.success_factor_id,
                    "metric_ids": activity.metric_ids,
                    "evidence_requirement_ids": (
                        activity.evidence_requirement_ids
                    ),
                }
                for activity in self.candidate_mel_mil_activities
            ],

            "candidate_exercise_activities": [
                {
                    "id": activity.id,
                    "title": activity.title,
                    "description": activity.description,
                    "delivery_method": activity.delivery_method,
                    "phase": activity.phase,
                    "notes": activity.notes,
                    "design_opportunity_id": activity.design_opportunity_id,
                    "cto_id": activity.cto_id,
                    "collective_task_id": activity.collective_task_id,
                    "success_factor_id": activity.success_factor_id,
                    "metric_ids": activity.metric_ids,
                    "evidence_requirement_ids": (
                        activity.evidence_requirement_ids
                    ),
                }
                for activity in self.candidate_exercise_activities
            ],

            "exercise_design_opportunities": [
                {
                    "id": opportunity.id,
                    "title": opportunity.title,
                    "description": opportunity.description,
                    "required_conditions": opportunity.required_conditions,
                    "stimulus_information": opportunity.stimulus_information,
                    "response_opportunity": opportunity.response_opportunity,
                    "evidence_capture_plan": opportunity.evidence_capture_plan,
                    "cto_id": opportunity.cto_id,
                    "collective_task_id": opportunity.collective_task_id,
                    "success_factor_id": opportunity.success_factor_id,
                    "metric_ids": opportunity.metric_ids,
                    "evidence_requirement_ids": (
                        opportunity.evidence_requirement_ids
                    ),
                }
                for opportunity in self.exercise_design_opportunities
            ],

            "collective_training_objectives": [
    {
        "id": cto.id,
        "title": cto.title,
        "training_audience": cto.training_audience,
        "required_outcome": cto.required_outcome,
        "conditions": cto.conditions,
        "challenge_level": cto.challenge_level,
        "contributing_functions": cto.contributing_functions,
        "individual_contributions": cto.individual_contributions,

        "evidence_requirements": [
            {
                "id": requirement.id,
                "description": requirement.description,
                "evidence_type": requirement.evidence_type,
                "notes": requirement.notes,
            }
            for requirement in cto.evidence_requirements
        ],

        "collective_tasks": [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,

                "success_factors": [
                    {
                        "id": factor.id,
                        "description": factor.description,
                        "metrics": [
                            {
                                "id": metric.id,
                                "description": metric.description,
                                "category": metric.category,
                                "evidence_requirements": [
                                    {
                                        "id": requirement.id,
                                        "description": requirement.description,
                                        "evidence_type": requirement.evidence_type,
                                        "notes": requirement.notes,
                                    }
                                    for requirement
                                    in metric.evidence_requirements
                                ],
                            }
                            for metric in factor.metrics
                        ],
                    }
                    for factor in task.success_factors
                ],

                "critical_errors": [
                    {
                        "id": error.id,
                        "description": error.description,
                        "metrics": [
                            {
                                "id": metric.id,
                                "description": metric.description,
                                "category": metric.category,
                                "evidence_requirements": [
                                    {
                                        "id": requirement.id,
                                        "description": requirement.description,
                                        "evidence_type": requirement.evidence_type,
                                        "notes": requirement.notes,
                                    }
                                    for requirement
                                    in metric.evidence_requirements
                                ],
                            }
                            for metric in error.metrics
                        ],
                    }
                    for error in task.critical_errors
                ],
            }
            for task in cto.collective_tasks
        ],
    }
    for cto in self.collective_training_objectives
],

            "observations": [
                {
                    "observation_id": observation.observation_id,
                    "exercise_time": observation.exercise_time,
                    "observed_at": observation.observed_at,
                    "observer_name": observation.observer_name,
                    "grid_reference": observation.grid_reference,
                    "latitude": observation.latitude,
                    "longitude": observation.longitude,
                    "location_description": (
                        observation.location_description
                    ),
                    "observer_role": observation.observer_role,
                    "observation_type": (
                        observation.observation_type.value
                    ),
                    "title": observation.title,
                    "description": observation.description,
                    "related_inject_number": (
                        observation.related_inject_number
                    ),
                    "related_objective_titles": (
                        observation.related_objective_titles
                    ),
                    "related_activity_id": (
                        observation.related_activity_id
                    ),
                    "evidence_ids": observation.evidence_ids,
                    "status": observation.status.value,
                    "recorded_at": observation.recorded_at,
                    "reviewed_by": observation.reviewed_by,
                    "reviewed_at": observation.reviewed_at,
                    "withdrawal_reason": (
                        observation.withdrawal_reason
                    ),
                    "withdrawn_by": observation.withdrawn_by,
                    "withdrawn_at": observation.withdrawn_at,
                }
                for observation in self.observations
            ],

            "evidence_records": [
                {
                    "evidence_id": evidence.evidence_id,
                    "title": evidence.title,
                    "evidence_type": evidence.evidence_type.value,
                    "description": evidence.description,
                    "source": evidence.source,
                    "related_standard": evidence.related_standard,
                    "related_objective": evidence.related_objective,
                    "related_inject": evidence.related_inject,
                    "recorded_by": evidence.recorded_by,
                    "recorded_at": evidence.recorded_at,
                    "reference": evidence.reference,
                }
                for evidence in self.evidence_records
            ],

                    "assessment_records": [
                {
                    "assessment_id": assessment.assessment_id,
                    "inject_number": assessment.inject_number,
                    "objective_title": assessment.objective_title,
                    "cto_id": assessment.cto_id,
                    "collective_task_id": (
                        assessment.collective_task_id
                    ),
                    "success_factor_id": (
                        assessment.success_factor_id
                    ),
                    "metric_ids": assessment.metric_ids,
                    "evidence_requirement_ids": (
                        assessment.evidence_requirement_ids
                    ),
                    "outcome": assessment.outcome.value,
                    "evidence_ids": assessment.evidence_ids,
                    "comments": assessment.comments,
                    "assessor": assessment.assessor,
                    "recorded_at": assessment.recorded_at,
                }
                for assessment in self.assessment_records
            ],
                        "confidence_assessments": [
                {
                    "assessment_id": (
                        assessment.assessment_id
                    ),
                    "exercise_id": (
                        assessment.exercise_id
                    ),
                    "scope": assessment.scope.value,
                    "subject_id": assessment.subject_id,
                    "related_objective_ids": (
                        assessment.related_objective_ids
                    ),
                    "stage": assessment.stage.value,
                    "confidence_score": (
                        assessment.confidence_score
                    ),
                    "reflection": assessment.reflection,
                    "recorded_at": assessment.recorded_at,
                }
                for assessment
                in self.confidence_assessments
            ],

            "learning_events": [
                {
                    "learning_event_id": (
                        event.learning_event_id
                    ),
                    "exercise_id": event.exercise_id,
                    "scope": event.scope.value,
                    "subject_id": event.subject_id,
                    "title": event.title,
                    "description": event.description,
                    "related_objective_ids": (
                        event.related_objective_ids
                    ),
                    "state": event.state.value,
                    "related_evidence_ids": (
                        event.related_evidence_ids
                    ),
                    "subsequent_evidence_ids": (
                        event.subsequent_evidence_ids
                    ),
                    "reflection": event.reflection,
                    "recorded_by": event.recorded_by,
                    "recorded_at": event.recorded_at,
                }
                for event in self.learning_events
            ],

            "demonstrated_strengths": [
                {
                    "strength_id": strength.strength_id,
                    "exercise_id": strength.exercise_id,
                    "scope": strength.scope.value,
                    "subject_id": strength.subject_id,
                    "title": strength.title,
                    "description": strength.description,
                    "related_objective_ids": (
                        strength.related_objective_ids
                    ),
                    "related_evidence_ids": (
                        strength.related_evidence_ids
                    ),
                    "identified_by": (
                        strength.identified_by
                    ),
                    "recorded_at": strength.recorded_at,
                }
                for strength
                in self.demonstrated_strengths
            ],

            "readiness_decisions": [
                {
                    "decision_id": decision.decision_id,
                    "outcome": decision.outcome.value,
                    "assessment_ids": decision.assessment_ids,
                    "rationale": decision.rationale,
                    "limitations": decision.limitations,
                    "required_action": decision.required_action,
                    "decision_maker": decision.decision_maker,
                    "decision_authority": decision.decision_authority,
                    "recorded_at": decision.recorded_at,
                    "exception_reason": (
                        decision.exception_reason.value
                        if decision.exception_reason
                        else None
                    ),
                    "exception_explanation": (
                        decision.exception_explanation
                    ),
                }
                for decision in self.readiness_decisions
            ],

            "findings": [
                {
                    "finding_id": finding.finding_id,
                    "title": finding.title,
                    "finding_type": finding.finding_type.value,
                    "description": finding.description,
                    "related_decision_id": (
                        finding.related_decision_id
                    ),
                    "related_assessment_ids": (
                        finding.related_assessment_ids
                    ),
                    "related_evidence_ids": (
                        finding.related_evidence_ids
                    ),
                    "recorded_by": finding.recorded_by,
                    "recorded_at": finding.recorded_at,
                }
                for finding in self.findings
            ],
            "recommendations": [
                {
                    "recommendation_id": recommendation.recommendation_id,
                    "title": recommendation.title,
                    "recommendation_type": (
                        recommendation.recommendation_type.value
                    ),
                    "description": recommendation.description,
                    "related_finding_ids": (
                        recommendation.related_finding_ids
                    ),
                    "disposition": recommendation.disposition.value,
                    "disposition_rationale": (
                        recommendation.disposition_rationale
                    ),
                    "disposition_by": recommendation.disposition_by,
                    "disposition_authority": (
                        recommendation.disposition_authority
                    ),
                    "disposition_at": recommendation.disposition_at,
                    "recommended_by": recommendation.recommended_by,
                    "recorded_at": recommendation.recorded_at,
                }
                for recommendation in self.recommendations
            ],

            "improvement_actions": [
                {
                    "action_id": action.action_id,
                    "title": action.title,
                    "description": action.description,
                    "related_recommendation_ids": (
                        action.related_recommendation_ids
                    ),
                     "related_finding_ids": (
                        action.related_finding_ids
                    ),
                    "related_verification_ids": (
                        action.related_verification_ids
                    ),
                    "owner": action.owner,
                    "priority": action.priority.value,
                    "target_date": action.target_date,
                    "status": action.status.value,
                    "completion_notes": action.completion_notes,
                    "completion_evidence_ids": (
                        action.completion_evidence_ids
                    ),
                    "authorised_by": action.authorised_by,
                    "authorised_at": action.authorised_at,
                    "completed_by": action.completed_by,
                    "completed_at": action.completed_at,
                }
                for action in self.improvement_actions
            ],

            "improvement_verifications": [
                {
                    "verification_id": verification.verification_id,
                    "related_action_id": verification.related_action_id,
                    "related_finding_ids": verification.related_finding_ids,
                    "related_evidence_ids": verification.related_evidence_ids,
                    "outcome": verification.outcome.value,
                    "rationale": verification.rationale,
                    "assessed_by": verification.assessed_by,
                    "assessment_authority": (
                        verification.assessment_authority
                    ),
                    "recorded_at": verification.recorded_at,
                }
                for verification in self.improvement_verifications
            ],

            "training_opportunities": [
                {
                    "opportunity_id": opportunity.opportunity_id,
                    "title": opportunity.title,
                    "organisation": opportunity.organisation,
                    "description": opportunity.description,
                    "start_date": opportunity.start_date,
                    "end_date": opportunity.end_date,
                    "location": opportunity.location,
                    "status": opportunity.status.value,
                    "related_finding_ids": (
                        opportunity.related_finding_ids
                    ),
                    "related_recommendation_ids": (
                        opportunity.related_recommendation_ids
                    ),
                    "related_action_ids": (
                        opportunity.related_action_ids
                    ),
                    "suitability_rationale": (
                        opportunity.suitability_rationale
                    ),
                    "access_confirmed": opportunity.access_confirmed,
                    "assessment_arrangements_confirmed": (
                        opportunity.assessment_arrangements_confirmed
                    ),
                    "point_of_contact": opportunity.point_of_contact,
                    "identified_by": opportunity.identified_by,
                    "identified_at": opportunity.identified_at,
                    "validated_by": opportunity.validated_by,
                    "validated_at": opportunity.validated_at,
                }
                for opportunity in self.training_opportunities
            ],
            "candidate_opportunities": [
                {
                    "candidate_id": candidate.candidate_id,
                    "title": candidate.title,
                    "organisation": candidate.organisation,
                    "description": candidate.description,
                    "start_date": candidate.start_date,
                    "end_date": candidate.end_date,
                    "location": candidate.location,
                    "source_type": candidate.source_type.value,
                    "source_name": candidate.source_name,
                    "source_reference": candidate.source_reference,
                    "status": candidate.status.value,
                    "related_finding_ids": (
                        candidate.related_finding_ids
                    ),
                    "related_recommendation_ids": (
                        candidate.related_recommendation_ids
                    ),
                    "related_action_ids": (
                        candidate.related_action_ids
                    ),
                    "relevance_reasons": (
                        candidate.relevance_reasons
                    ),
                    "review_reason": candidate.review_reason,
                    "review_notes": candidate.review_notes,
                    "reviewed_by": candidate.reviewed_by,
                    "reviewed_at": candidate.reviewed_at,
                    "identified_at": candidate.identified_at,
                    "promoted_opportunity_id": (
                        candidate.promoted_opportunity_id
                    ),
                }
                for candidate in self.candidate_opportunities
            ],

                        "planning_sources": [
                {
                    "source_id": source.source_id,
                    "name": source.name,
                    "organisation": source.organisation,
                    "source_type": source.source_type.value,
                    "description": source.description,
                    "reference": source.reference,
                    "status": source.status.value,
                    "authorised_for_discovery": (
                        source.authorised_for_discovery
                    ),
                    "authorised_by": source.authorised_by,
                    "authority": source.authority,
                    "authorised_at": source.authorised_at,
                    "authorisation_notes": (
                        source.authorisation_notes
                    ),
                    "suspended_by": source.suspended_by,
                    "suspended_at": source.suspended_at,
                    "suspension_reason": (
                        source.suspension_reason
                    ),
                    "withdrawn_by": source.withdrawn_by,
                    "withdrawn_at": source.withdrawn_at,
                    "withdrawal_reason": (
                        source.withdrawal_reason
                    ),
                }
                for source in self.planning_sources
            ],

            "planned_activities": [
                {
                    "activity_id": activity.activity_id,
                    "title": activity.title,
                    "organisation": activity.organisation,
                    "description": activity.description,
                    "start_date": activity.start_date,
                    "end_date": activity.end_date,
                    "location": activity.location,
                    "source_type": activity.source_type.value,
                    "source_name": activity.source_name,
                    "source_reference": (
                        activity.source_reference
                    ),
                    "activity_tags": activity.activity_tags,
                    "capability_tags": (
                        activity.capability_tags
                    ),
                    "participants": activity.participants,
                }
                for activity in self.planned_activities
            ],

            "discovery_requirements": [
                {
                    "requirement_id": requirement.requirement_id,
                    "title": requirement.title,
                    "description": requirement.description,
                    "capability_area": requirement.capability_area,
                    "required_activities": (
                        requirement.required_activities
                    ),
                    "desired_evidence": (
                        requirement.desired_evidence
                    ),
                    "keywords": requirement.keywords,
                    "earliest_date": requirement.earliest_date,
                    "latest_date": requirement.latest_date,
                    "related_finding_ids": (
                        requirement.related_finding_ids
                    ),
                    "related_recommendation_ids": (
                        requirement.related_recommendation_ids
                    ),
                    "related_action_ids": (
                        requirement.related_action_ids
                    ),
                }
                for requirement in self.discovery_requirements
            ],
            
            "design_trace_records": [
                {
                    "trace_id": record.trace_id,
                    "event_type": record.event_type.value,
                    "objective_title": (
                        record.objective_title
                    ),
                    "proposal_id": record.proposal_id,
                    "summary": record.summary,
                    "rationale": record.rationale,
                    "original_content": (
                        record.original_content
                    ),
                    "proposed_content": (
                        record.proposed_content
                    ),
                    "reviewed_content": (
                        record.reviewed_content
                    ),
                    "resulting_content": (
                        record.resulting_content
                    ),
                    "source_references": (
                        record.source_references
                    ),
                    "recorded_by": record.recorded_by,
                    "recorded_at": record.recorded_at,
                }
                for record in self.design_trace_records
            ],

            "injects": [
                {
                    "number": inject.number,
                    "title": inject.title,
                    "exercise_time": inject.exercise_time,
                    "phase": inject.phase,
                    "source": inject.source,
                    "method": inject.method,
                    "audience": inject.audience,
                    "category": inject.category,
                    "inject_text": inject.inject_text,
                    "expected_action": inject.expected_action,
                    "facilitator_notes": inject.facilitator_notes,
                    "attachments": inject.attachments,
                    "status": inject.status.value,
                }
                for inject in self.injects
            ],
        }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(project_data, file, indent=4)

    @classmethod
    def load(cls, filename):
        path = Path(filename)

        if not path.exists():
            raise FileNotFoundError("Project file not found")

        with open(filename, "r", encoding="utf-8") as file:
            project_data = json.load(file)

        project = cls(
            project_data.get("name", "Untitled Project")
        )

        saved_operational_requirement = project_data.get(
            "operational_requirement",
            {},
        )

        saved_readiness = saved_operational_requirement.get(
            "readiness",
            {},
        )

        saved_gap = saved_readiness.get(
            "readiness_gap",
            {},
        )

        # Backwards compatibility:
        # Older project files stored readiness_gap as a simple string.
        if isinstance(saved_gap, str):
            readiness_gap = ReadinessGap(
                shortfall=saved_gap
            )
        else:
            readiness_gap = ReadinessGap(
                required_standard=saved_gap.get(
                    "required_standard",
                    "",
                ),
                current_state=saved_gap.get(
                    "current_state",
                    "",
                ),
                shortfall=saved_gap.get(
                    "shortfall",
                    "",
                ),
                consequence=saved_gap.get(
                    "consequence",
                    "",
                ),
                preparation_requirement=saved_gap.get(
                    "preparation_requirement",
                    "",
                ),
                rationale=saved_gap.get(
                    "rationale",
                    "",
                ),
            )
        saved_improvement_actions = project_data.get(
            "improvement_actions",
            [],
        )

        project.improvement_actions = [
            ImprovementAction(
                action_id=item.get(
                    "action_id",
                    "",
                ),
                title=item.get(
                    "title",
                    "",
                ),
                description=item.get(
                    "description",
                    "",
                ),
                related_recommendation_ids=item.get(
                    "related_recommendation_ids",
                    [],
                ),
                related_finding_ids=item.get(
                    "related_finding_ids",
                    [],
                ),
                related_verification_ids=item.get(
                    "related_verification_ids",
                    [],
                ),
                owner=item.get(
                    "owner",
                    "",
                ),
                priority=cls._parse_action_priority(
                    item.get(
                        "priority",
                        ActionPriority.MEDIUM.value,
                    )
                ),
                target_date=item.get(
                    "target_date",
                    "",
                ),
                status=cls._parse_action_status(
                    item.get(
                        "status",
                        ActionStatus.NOT_STARTED.value,
                    )
                ),
                completion_notes=item.get(
                    "completion_notes",
                    "",
                ),
                completion_evidence_ids=item.get(
                    "completion_evidence_ids",
                    [],
                ),
                authorised_by=item.get(
                    "authorised_by",
                    "",
                ),
                authorised_at=item.get(
                    "authorised_at",
                    "",
                ),
                completed_by=item.get(
                    "completed_by",
                    "",
                ),
                completed_at=item.get(
                    "completed_at",
                    "",
                ),
            )
            for item in saved_improvement_actions
        ]

        for action in project.improvement_actions:
            if not action.action_id:
                action.action_id = str(uuid4())

        saved_improvement_verifications = project_data.get(
            "improvement_verifications",
            [],
        )

        project.improvement_verifications = [
            ImprovementVerification(
                verification_id=item.get("verification_id", ""),
                related_action_id=item.get("related_action_id", ""),
                related_finding_ids=item.get("related_finding_ids", []),
                related_evidence_ids=item.get("related_evidence_ids", []),
                outcome=cls._parse_verification_outcome(
                    item.get(
                        "outcome",
                        VerificationOutcome.INSUFFICIENT_EVIDENCE.value,
                    )
                ),
                rationale=item.get("rationale", ""),
                assessed_by=item.get("assessed_by", ""),
                assessment_authority=item.get(
                    "assessment_authority",
                    "",
                ),
                recorded_at=item.get("recorded_at", ""),
            )
            for item in saved_improvement_verifications
        ]

        for verification in project.improvement_verifications:
            if not verification.verification_id:
                verification.verification_id = str(uuid4())

        project.operational_requirement = OperationalRequirement(
            title=saved_operational_requirement.get(
                "title",
                "",
            ),
            description=saved_operational_requirement.get(
                "description",
                "",
            ),
            sponsor=saved_operational_requirement.get(
                "sponsor",
                "",
            ),
            operational_driver=saved_operational_requirement.get(
                "operational_driver",
                "",
            ),
            success_criteria=saved_operational_requirement.get(
                "success_criteria",
                "",
            ),
            doctrine_reference=saved_operational_requirement.get(
                "doctrine_reference"
            ),
            readiness=OperationalReadiness(
                current_state=saved_readiness.get(
                    "current_state",
                    "",
                ),
                required_state=saved_readiness.get(
                    "required_state",
                    "",
                ),
                required_standard=saved_readiness.get(
                    "required_standard",
                    "",
                ),
                readiness_gap=readiness_gap,
                rationale=saved_readiness.get(
                    "rationale",
                    "",
                ),
            ),
        )

        saved_doctrine_references = project_data.get(
            "doctrine_references",
            [],
        )
        saved_training_opportunities = project_data.get(
            "training_opportunities",
            [],
        )

        project.training_opportunities = [
            TrainingOpportunity(
                opportunity_id=item.get(
                    "opportunity_id",
                    "",
                ),
                title=item.get(
                    "title",
                    "",
                ),
                organisation=item.get(
                    "organisation",
                    "",
                ),
                description=item.get(
                    "description",
                    "",
                ),
                start_date=item.get(
                    "start_date",
                    "",
                ),
                end_date=item.get(
                    "end_date",
                    "",
                ),
                location=item.get(
                    "location",
                    "",
                ),
                status=cls._parse_training_opportunity_status(
                    item.get(
                        "status",
                        TrainingOpportunityStatus.POTENTIAL.value,
                    )
                ),
                related_finding_ids=item.get(
                    "related_finding_ids",
                    [],
                ),
                related_recommendation_ids=item.get(
                    "related_recommendation_ids",
                    [],
                ),
                related_action_ids=item.get(
                    "related_action_ids",
                    [],
                ),
                suitability_rationale=item.get(
                    "suitability_rationale",
                    "",
                ),
                access_confirmed=item.get(
                    "access_confirmed",
                    False,
                ),
                assessment_arrangements_confirmed=item.get(
                    "assessment_arrangements_confirmed",
                    False,
                ),
                point_of_contact=item.get(
                    "point_of_contact",
                    "",
                ),
                identified_by=item.get(
                    "identified_by",
                    "",
                ),
                identified_at=item.get(
                    "identified_at",
                    "",
                ),
                validated_by=item.get(
                    "validated_by",
                    "",
                ),
                validated_at=item.get(
                    "validated_at",
                    "",
                ),
            )
            for item in saved_training_opportunities
        ]

        for opportunity in project.training_opportunities:
            if not opportunity.opportunity_id:
                opportunity.opportunity_id = str(uuid4())
        project.doctrine_references = [
            DoctrineReference(
                title=item.get("title", ""),
                reference=item.get("reference", ""),
                version=item.get("version", ""),
                organisation=item.get("organisation", ""),
                description=item.get("description", ""),
                location=item.get("location", ""),
            )
            for item in saved_doctrine_references
        ]

        saved_objectives = project_data.get(
            "objectives",
            [],
        )

        saved_candidate_opportunities = project_data.get(
            "candidate_opportunities",
            [],
        )

        project.candidate_opportunities = [
            CandidateOpportunity(
                candidate_id=item.get(
                    "candidate_id",
                    "",
                ),
                title=item.get(
                    "title",
                    "",
                ),
                organisation=item.get(
                    "organisation",
                    "",
                ),
                description=item.get(
                    "description",
                    "",
                ),
                start_date=item.get(
                    "start_date",
                    "",
                ),
                end_date=item.get(
                    "end_date",
                    "",
                ),
                location=item.get(
                    "location",
                    "",
                ),
                source_type=cls._parse_opportunity_source_type(
                    item.get(
                        "source_type",
                        OpportunitySourceType.OTHER.value,
                    )
                ),
                source_name=item.get(
                    "source_name",
                    "",
                ),
                source_reference=item.get(
                    "source_reference",
                    "",
                ),
                status=cls._parse_candidate_status(
                    item.get(
                        "status",
                        CandidateStatus.DISCOVERED.value,
                    )
                ),
                related_finding_ids=item.get(
                    "related_finding_ids",
                    [],
                ),
                related_recommendation_ids=item.get(
                    "related_recommendation_ids",
                    [],
                ),
                related_action_ids=item.get(
                    "related_action_ids",
                    [],
                ),
                relevance_reasons=item.get(
                    "relevance_reasons",
                    [],
                ),
                review_reason=item.get(
                    "review_reason",
                    "",
                ),
                review_notes=item.get(
                    "review_notes",
                    "",
                ),
                reviewed_by=item.get(
                    "reviewed_by",
                    "",
                ),
                reviewed_at=item.get(
                    "reviewed_at",
                    "",
                ),
                identified_at=item.get(
                    "identified_at",
                    "",
                ),
                promoted_opportunity_id=item.get(
                    "promoted_opportunity_id",
                    "",
                ),
            )
            for item in saved_candidate_opportunities
        ]

        for candidate in project.candidate_opportunities:
            if not candidate.candidate_id:
                candidate.candidate_id = str(uuid4())


        saved_planning_sources = project_data.get(
            "planning_sources",
            [],
        )

        project.planning_sources = [
            PlanningSource(
                source_id=item.get(
                    "source_id",
                    "",
                ),
                name=item.get(
                    "name",
                    "",
                ),
                organisation=item.get(
                    "organisation",
                    "",
                ),
                source_type=cls._parse_planning_source_type(
                    item.get(
                        "source_type",
                        PlanningSourceType.OTHER.value,
                    )
                ),
                description=item.get(
                    "description",
                    "",
                ),
                reference=item.get(
                    "reference",
                    "",
                ),
                status=cls._parse_planning_source_status(
                    item.get(
                        "status",
                        PlanningSourceStatus.PROPOSED.value,
                    )
                ),
                authorised_for_discovery=item.get(
                    "authorised_for_discovery",
                    False,
                ),
                authorised_by=item.get(
                    "authorised_by",
                    "",
                ),
                authority=item.get(
                    "authority",
                    "",
                ),
                authorised_at=item.get(
                    "authorised_at",
                    "",
                ),
                authorisation_notes=item.get(
                    "authorisation_notes",
                    "",
                ),
                suspended_by=item.get(
                    "suspended_by",
                    "",
                ),
                suspended_at=item.get(
                    "suspended_at",
                    "",
                ),
                suspension_reason=item.get(
                    "suspension_reason",
                    "",
                ),
                withdrawn_by=item.get(
                    "withdrawn_by",
                    "",
                ),
                withdrawn_at=item.get(
                    "withdrawn_at",
                    "",
                ),
                withdrawal_reason=item.get(
                    "withdrawal_reason",
                    "",
                ),
            )
            for item in saved_planning_sources
        ]

        for source in project.planning_sources:
            if not source.source_id:
                source.source_id = str(uuid4())

        saved_discovery_requirements = project_data.get(
            "discovery_requirements",
            [],
        )

        project.discovery_requirements = [
            DiscoveryRequirement(
                requirement_id=item.get(
                    "requirement_id",
                    "",
                ),
                title=item.get(
                    "title",
                    "",
                ),
                description=item.get(
                    "description",
                    "",
                ),
                capability_area=item.get(
                    "capability_area",
                    "",
                ),
                required_activities=item.get(
                    "required_activities",
                    [],
                ),
                desired_evidence=item.get(
                    "desired_evidence",
                    [],
                ),
                keywords=item.get(
                    "keywords",
                    [],
                ),
                earliest_date=item.get(
                    "earliest_date",
                    "",
                ),
                latest_date=item.get(
                    "latest_date",
                    "",
                ),
                related_finding_ids=item.get(
                    "related_finding_ids",
                    [],
                ),
                related_recommendation_ids=item.get(
                    "related_recommendation_ids",
                    [],
                ),
                related_action_ids=item.get(
                    "related_action_ids",
                    [],
                ),
            )
        for item in saved_discovery_requirements
        ]

        for requirement in project.discovery_requirements:
            if not requirement.requirement_id:
                requirement.requirement_id = str(uuid4())

        saved_planned_activities = project_data.get(
            "planned_activities",
            [],
        )

        project.planned_activities = [
            PlannedActivity(
                activity_id=item.get(
                    "activity_id",
                    "",
                ),
                title=item.get(
                    "title",
                    "",
                ),
                organisation=item.get(
                    "organisation",
                    "",
                ),
                description=item.get(
                    "description",
                    "",
                ),
                start_date=item.get(
                    "start_date",
                    "",
                ),
                end_date=item.get(
                    "end_date",
                    "",
                ),
                location=item.get(
                    "location",
                    "",
                ),
                source_type=cls._parse_planned_activity_source_type(
                    item.get(
                        "source_type",
                        PlannedActivitySourceType.OTHER.value,
                    )
                ),
                source_name=item.get(
                    "source_name",
                    "",
                ),
                source_reference=item.get(
                    "source_reference",
                    "",
                ),
                activity_tags=item.get(
                    "activity_tags",
                    [],
                ),
                capability_tags=item.get(
                    "capability_tags",
                    [],
                ),
                participants=item.get(
                    "participants",
                    [],
                ),
            )
            for item in saved_planned_activities
        ]

        for activity in project.planned_activities:
            if not activity.activity_id:
                activity.activity_id = str(uuid4())

        project.objectives = [
            ExerciseObjective(
                title=item.get("title", ""),
                description=item.get("description", ""),
                success_criteria=item.get(
                    "success_criteria",
                    [],
                ),
                supporting_injects=item.get(
                    "supporting_injects",
                    [],
                ),
                achieved=item.get("achieved"),
            )
            for item in saved_objectives
        ]
        
        saved_design_trace_records = project_data.get(
            "design_trace_records",
            [],
        )

        project.design_trace_records = [
            DesignTraceRecord(
                trace_id=item.get(
                    "trace_id",
                    str(uuid4()),
                ),
                event_type=cls._parse_design_trace_event_type(
                    item.get(
                        "event_type",
                        DesignTraceEventType.ATTENTION_IDENTIFIED.value,
                    )
                ),
                objective_title=item.get(
                    "objective_title",
                    "",
                ),
                proposal_id=item.get(
                    "proposal_id",
                    "",
                ),
                summary=item.get(
                    "summary",
                    "",
                ),
                rationale=item.get(
                    "rationale",
                    "",
                ),
                original_content=item.get(
                    "original_content",
                    [],
                ),
                proposed_content=item.get(
                    "proposed_content",
                    [],
                ),
                reviewed_content=item.get(
                    "reviewed_content",
                    [],
                ),
                resulting_content=item.get(
                    "resulting_content",
                    [],
                ),
                source_references=item.get(
                    "source_references",
                    [],
                ),
                recorded_by=item.get(
                    "recorded_by",
                    "",
                ),
                recorded_at=item.get(
                    "recorded_at",
                    "",
                ),
            )
            for item in saved_design_trace_records
        ]
        saved_mel_mil_promotions = project_data.get(
            "mel_mil_promotions",
            [],
        )

        project.mel_mil_promotions = [
            MelMilPromotion(
                id=item.get("id") or str(uuid4()),
                inject_number=item.get(
                    "inject_number",
                    0,
                ),
                candidate_mel_mil_activity_id=item.get(
                    "candidate_mel_mil_activity_id",
                    "",
                ),
                candidate_activity_id=item.get(
                    "candidate_activity_id",
                    "",
                ),
                design_opportunity_id=item.get(
                    "design_opportunity_id",
                    "",
                ),
                cto_id=item.get("cto_id", ""),
                collective_task_id=item.get(
                    "collective_task_id",
                    "",
                ),
                success_factor_id=item.get(
                    "success_factor_id",
                    "",
                ),
                metric_ids=item.get(
                    "metric_ids",
                    [],
                ),
                evidence_requirement_ids=item.get(
                    "evidence_requirement_ids",
                    [],
                ),
            )
            for item in saved_mel_mil_promotions
        ]

        saved_candidate_mel_mil = project_data.get(
            "candidate_mel_mil_activities",
            [],
        )

        project.candidate_mel_mil_activities = [
            CandidateMelMilActivity(
                id=item.get("id") or str(uuid4()),
                title=item.get("title", ""),
                activity_type=item.get(
                    "activity_type",
                    "",
                ),
                phase=item.get("phase", ""),
                timing_window=item.get(
                    "timing_window",
                    "",
                ),
                event_summary=item.get(
                    "event_summary",
                    "",
                ),
                intended_effect=item.get(
                    "intended_effect",
                    "",
                ),
                control_notes=item.get(
                    "control_notes",
                    "",
                ),
                candidate_activity_id=item.get(
                    "candidate_activity_id",
                    "",
                ),
                design_opportunity_id=item.get(
                    "design_opportunity_id",
                    "",
                ),
                cto_id=item.get("cto_id", ""),
                collective_task_id=item.get(
                    "collective_task_id",
                    "",
                ),
                success_factor_id=item.get(
                    "success_factor_id",
                    "",
                ),
                metric_ids=item.get(
                    "metric_ids",
                    [],
                ),
                evidence_requirement_ids=item.get(
                    "evidence_requirement_ids",
                    [],
                ),
            )
            for item in saved_candidate_mel_mil
        ]

        saved_candidate_activities = project_data.get(
            "candidate_exercise_activities",
            [],
        )

        project.candidate_exercise_activities = [
            CandidateExerciseActivity(
                id=item.get("id") or str(uuid4()),
                title=item.get("title", ""),
                description=item.get("description", ""),
                delivery_method=item.get(
                    "delivery_method",
                    "",
                ),
                phase=item.get("phase", ""),
                notes=item.get("notes", ""),
                design_opportunity_id=item.get(
                    "design_opportunity_id",
                    "",
                ),
                cto_id=item.get("cto_id", ""),
                collective_task_id=item.get(
                    "collective_task_id",
                    "",
                ),
                success_factor_id=item.get(
                    "success_factor_id",
                    "",
                ),
                metric_ids=item.get(
                    "metric_ids",
                    [],
                ),
                evidence_requirement_ids=item.get(
                    "evidence_requirement_ids",
                    [],
                ),
            )
            for item in saved_candidate_activities
        ]

        saved_design_opportunities = project_data.get(
            "exercise_design_opportunities",
            [],
        )

        project.exercise_design_opportunities = [
            ExerciseDesignOpportunity(
                id=item.get("id") or str(uuid4()),
                title=item.get("title", ""),
                description=item.get("description", ""),
                required_conditions=item.get(
                    "required_conditions",
                    "",
                ),
                stimulus_information=item.get(
                    "stimulus_information",
                    "",
                ),
                response_opportunity=item.get(
                    "response_opportunity",
                    "",
                ),
                evidence_capture_plan=item.get(
                    "evidence_capture_plan",
                    "",
                ),
                cto_id=item.get("cto_id", ""),
                collective_task_id=item.get(
                    "collective_task_id",
                    "",
                ),
                success_factor_id=item.get(
                    "success_factor_id",
                    "",
                ),
                metric_ids=item.get(
                    "metric_ids",
                    [],
                ),
                evidence_requirement_ids=item.get(
                    "evidence_requirement_ids",
                    [],
                ),
            )
            for item in saved_design_opportunities
        ]

        saved_ctos = project_data.get(
            "collective_training_objectives",
            [],
        )

        project.collective_training_objectives = []

        for cto_data in saved_ctos:
            cto = CollectiveTrainingObjective(
                id=cto_data.get("id") or str(uuid4()),
                title=cto_data.get("title", ""),
                training_audience=cto_data.get(
                    "training_audience",
                    "",
                ),
                required_outcome=cto_data.get(
                    "required_outcome",
                    "",
                ),
                conditions=cto_data.get(
                    "conditions",
                    "",
                ),
                challenge_level=cto_data.get(
                    "challenge_level"
                ),
                contributing_functions=cto_data.get(
                    "contributing_functions",
                    [],
                ),
                individual_contributions=cto_data.get(
                    "individual_contributions",
                    [],
                ),
            )

            cto.evidence_requirements = [
                EvidenceRequirement(
                    id=item.get("id") or str(uuid4()),
                    description=item.get(
                        "description",
                        "",
                    ),
                    evidence_type=item.get(
                        "evidence_type",
                        "",
                    ),
                    notes=item.get(
                        "notes",
                        "",
                    ),
                )
                for item in cto_data.get(
                    "evidence_requirements",
                    [],
                )
            ]

            for task_data in cto_data.get(
                "collective_tasks",
                [],
            ):
                task = CollectiveTask(
                    id=task_data.get("id") or str(uuid4()),
                    title=task_data.get("title", ""),
                    description=task_data.get(
                        "description",
                        "",
                    ),
                )

                for factor_data in task_data.get(
                    "success_factors",
                    [],
                ):
                    factor = SuccessFactor(
                        id=factor_data.get("id") or str(uuid4()),
                        description=factor_data.get(
                            "description",
                            "",
                        ),
                    )

                    for metric_data in factor_data.get(
                        "metrics",
                        [],
                    ):
                        metric = PerformanceMetric(
                            id=(
                                metric_data.get("id")
                                or str(uuid4())
                            ),
                            description=metric_data.get(
                                "description",
                                "",
                            ),
                            category=metric_data.get(
                                "category",
                                "",
                            ),
                        )

                        metric.evidence_requirements = [
                            EvidenceRequirement(
                                id=(
                                    item.get("id")
                                    or str(uuid4())
                                ),
                                description=item.get(
                                    "description",
                                    "",
                                ),
                                evidence_type=item.get(
                                    "evidence_type",
                                    "",
                                ),
                                notes=item.get(
                                    "notes",
                                    "",
                                ),
                            )
                            for item in metric_data.get(
                                "evidence_requirements",
                                [],
                            )
                        ]

                        factor.metrics.append(metric)

                    task.success_factors.append(factor)

                for error_data in task_data.get(
                    "critical_errors",
                    [],
                ):
                    error = CriticalError(
                        id=error_data.get("id") or str(uuid4()),
                        description=error_data.get(
                            "description",
                            "",
                        ),
                    )

                    for metric_data in error_data.get(
                        "metrics",
                        [],
                    ):
                        metric = PerformanceMetric(
                            id=(
                                metric_data.get("id")
                                or str(uuid4())
                            ),
                            description=metric_data.get(
                                "description",
                                "",
                            ),
                            category=metric_data.get(
                                "category",
                                "",
                            ),
                        )

                        metric.evidence_requirements = [
                            EvidenceRequirement(
                                id=(
                                    item.get("id")
                                    or str(uuid4())
                                ),
                                description=item.get(
                                    "description",
                                    "",
                                ),
                                evidence_type=item.get(
                                    "evidence_type",
                                    "",
                                ),
                                notes=item.get(
                                    "notes",
                                    "",
                                ),
                            )
                            for item in metric_data.get(
                                "evidence_requirements",
                                [],
                            )
                        ]

                        error.metrics.append(metric)

                    task.critical_errors.append(error)

                cto.collective_tasks.append(task)

            project.collective_training_objectives.append(
                cto
            )

        saved_evidence_records = project_data.get(
            "evidence_records",
            [],
        )

        project.evidence_records = [
            EvidenceRecord(
                evidence_id=item.get("evidence_id", ""),
                title=item.get("title", ""),
                evidence_type=cls._parse_evidence_type(
                    item.get(
                        "evidence_type",
                        EvidenceType.OBSERVATION.value,
                    )
                ),
                description=item.get("description", ""),
                source=item.get("source", ""),
                related_standard=item.get(
                    "related_standard",
                    "",
                ),
                related_objective=item.get(
                    "related_objective",
                    "",
                ),
                related_inject=item.get(
                    "related_inject"
                ),
                recorded_by=item.get(
                    "recorded_by",
                    "",
                ),
                recorded_at=item.get(
                    "recorded_at",
                    "",
                ),
                reference=item.get(
                    "reference",
                    "",
                ),
            )
            for item in saved_evidence_records
        ]

        for evidence in project.evidence_records:
            if not evidence.evidence_id:
                evidence.evidence_id = str(uuid4())

        saved_observations = project_data.get(
            "observations",
            [],
        )

        project.observations = [
        Observation(
            observation_id=item.get(
                "observation_id",
                "",
            ),
            exercise_time=item.get(
                "exercise_time",
                "",
            ),
            observed_at=item.get(
                "observed_at",
                "",
            ),
            observer_name=item.get(
                "observer_name",
                "",
            ),
            observer_role=item.get(
                "observer_role",
                "",
            ),
            grid_reference=item.get(
                "grid_reference",
                "",
            ),
            latitude=item.get(
                "latitude"
            ),
            longitude=item.get(
                "longitude"
            ),
            location_description=item.get(
                "location_description",
                "",
            ),
            observation_type=cls._parse_observation_type(
                item.get(
                    "observation_type",
                    ObservationType.OBSERVATION.value,
                )
            ),
            title=item.get(
                "title",
                "",
            ),
            description=item.get(
                "description",
                "",
            ),
            related_inject_number=item.get(
                "related_inject_number"
            ),
            related_objective_titles=item.get(
                "related_objective_titles",
                [],
            ),
            related_activity_id=item.get(
                "related_activity_id",
                "",
            ),
            evidence_ids=item.get(
                "evidence_ids",
                [],
            ),
            status=cls._parse_observation_status(
                item.get(
                    "status",
                    ObservationStatus.DRAFT.value,
                )
            ),
            recorded_at=item.get(
                "recorded_at",
                "",
            ),
            reviewed_by=item.get(
                "reviewed_by",
                "",
            ),
            reviewed_at=item.get(
                "reviewed_at",
                "",
            ),
            withdrawal_reason=item.get(
                "withdrawal_reason",
                "",
            ),
            withdrawn_by=item.get(
                "withdrawn_by",
                "",
            ),
            withdrawn_at=item.get(
                "withdrawn_at",
                "",
            ),
        )
        for item in saved_observations
    ]

        for observation in project.observations:
            if not observation.observation_id:
                observation.observation_id = str(uuid4())

        saved_confidence_assessments = project_data.get(
            "confidence_assessments",
            [],
        )

        project.confidence_assessments = [
            ConfidenceAssessment(
                assessment_id=item.get(
                    "assessment_id",
                    "",
                ),
                exercise_id=item.get(
                    "exercise_id",
                    "",
                ),
                scope=cls._parse_preparedness_scope(
                    item.get(
                        "scope",
                        PreparednessScope.INDIVIDUAL.value,
                    )
                ),
                subject_id=item.get(
                    "subject_id",
                    "",
                ),
                related_objective_ids=item.get(
                    "related_objective_ids",
                    [],
                ),
                stage=cls._parse_confidence_stage(
                    item.get(
                        "stage",
                        ConfidenceStage.PRE_EXERCISE.value,
                    )
                ),
                confidence_score=item.get(
                    "confidence_score"
                ),
                reflection=item.get(
                    "reflection",
                    "",
                ),
                recorded_at=item.get(
                    "recorded_at",
                    "",
                ),
            )
            for item in saved_confidence_assessments
        ]

        for assessment in project.confidence_assessments:
            if not assessment.assessment_id:
                assessment.assessment_id = str(uuid4())

        saved_learning_events = project_data.get(
            "learning_events",
            [],
        )

        project.learning_events = [
            LearningEvent(
                learning_event_id=item.get(
                    "learning_event_id",
                    "",
                ),
                exercise_id=item.get(
                    "exercise_id",
                    "",
                ),
                scope=cls._parse_preparedness_scope(
                    item.get(
                        "scope",
                        PreparednessScope.INDIVIDUAL.value,
                    )
                ),
                subject_id=item.get(
                    "subject_id",
                    "",
                ),
                title=item.get(
                    "title",
                    "",
                ),
                description=item.get(
                    "description",
                    "",
                ),
                related_objective_ids=item.get(
                    "related_objective_ids",
                    [],
                ),
                state=cls._parse_learning_opportunity_state(
                    item.get(
                        "state",
                        LearningOpportunityState.RECEIVED.value,
                    )
                ),
                related_evidence_ids=item.get(
                    "related_evidence_ids",
                    [],
                ),
                subsequent_evidence_ids=item.get(
                    "subsequent_evidence_ids",
                    [],
                ),
                reflection=item.get(
                    "reflection",
                    "",
                ),
                recorded_by=item.get(
                    "recorded_by",
                    "",
                ),
                recorded_at=item.get(
                    "recorded_at",
                    "",
                ),
            )
            for item in saved_learning_events
        ]

        for event in project.learning_events:
            if not event.learning_event_id:
                event.learning_event_id = str(uuid4())

        saved_demonstrated_strengths = project_data.get(
            "demonstrated_strengths",
            [],
        )

        project.demonstrated_strengths = [
            DemonstratedStrength(
                strength_id=item.get(
                    "strength_id",
                    "",
                ),
                exercise_id=item.get(
                    "exercise_id",
                    "",
                ),
                scope=cls._parse_preparedness_scope(
                    item.get(
                        "scope",
                        PreparednessScope.INDIVIDUAL.value,
                    )
                ),
                subject_id=item.get(
                    "subject_id",
                    "",
                ),
                title=item.get(
                    "title",
                    "",
                ),
                description=item.get(
                    "description",
                    "",
                ),
                related_objective_ids=item.get(
                    "related_objective_ids",
                    [],
                ),
                related_evidence_ids=item.get(
                    "related_evidence_ids",
                    [],
                ),
                identified_by=item.get(
                    "identified_by",
                    "",
                ),
                recorded_at=item.get(
                    "recorded_at",
                    "",
                ),
            )
            for item in saved_demonstrated_strengths
        ]

        for strength in project.demonstrated_strengths:
            if not strength.strength_id:
                strength.strength_id = str(uuid4())
                
        saved_assessment_records = project_data.get(
            "assessment_records",
            [],
        )

        project.assessment_records = [
            AssessmentRecord(
                assessment_id=item.get("assessment_id", ""),
                inject_number=item.get(
                    "inject_number",
                    0,
                ),
                objective_title=item.get(
                    "objective_title",
                    "",
                ),
                cto_id=item.get(
                    "cto_id",
                    "",
                ),
                collective_task_id=item.get(
                    "collective_task_id",
                    "",
                ),
                success_factor_id=item.get(
                    "success_factor_id",
                    "",
                ),
                metric_ids=item.get(
                    "metric_ids",
                    [],
                ),
                evidence_requirement_ids=item.get(
                    "evidence_requirement_ids",
                    [],
                ),
                outcome=cls._parse_assessment_outcome(
                    item.get(
                        "outcome",
                        AssessmentOutcome.NOT_ASSESSED.value,
                    )
                ),
                evidence_ids=item.get(
                    "evidence_ids",
                    [],
                ),
                comments=item.get(
                    "comments",
                    "",
                ),
                assessor=item.get(
                    "assessor",
                    "",
                ),
                recorded_at=item.get(
                    "recorded_at",
                    "",
                ),
            )
            for item in saved_assessment_records
        ]

        for assessment in project.assessment_records:
            if not assessment.assessment_id:
                assessment.assessment_id = str(uuid4())
                
                
        saved_confidence_assessments = project_data.get(
            "confidence_assessments",
            [],
        )

        project.confidence_assessments = [
            ConfidenceAssessment(
                assessment_id=item.get(
                    "assessment_id",
                    "",
                ),
                exercise_id=item.get(
                    "exercise_id",
                    "",
                ),
                scope=cls._parse_preparedness_scope(
                    item.get(
                        "scope",
                        PreparednessScope.INDIVIDUAL.value,
                    )
                ),
                subject_id=item.get(
                    "subject_id",
                    "",
                ),
                related_objective_ids=item.get(
                    "related_objective_ids",
                    [],
                ),
                stage=cls._parse_confidence_stage(
                    item.get(
                        "stage",
                        ConfidenceStage.PRE_EXERCISE.value,
                    )
                ),
                confidence_score=item.get(
                    "confidence_score"
                ),
                reflection=item.get(
                    "reflection",
                    "",
                ),
                recorded_at=item.get(
                    "recorded_at",
                    "",
                ),
            )
            for item in saved_confidence_assessments
        ]

        for assessment in project.confidence_assessments:
            if not assessment.assessment_id:
                assessment.assessment_id = str(uuid4())

        saved_learning_events = project_data.get(
            "learning_events",
            [],
        )

        project.learning_events = [
            LearningEvent(
                learning_event_id=item.get(
                    "learning_event_id",
                    "",
                ),
                exercise_id=item.get(
                    "exercise_id",
                    "",
                ),
                scope=cls._parse_preparedness_scope(
                    item.get(
                        "scope",
                        PreparednessScope.INDIVIDUAL.value,
                    )
                ),
                subject_id=item.get(
                    "subject_id",
                    "",
                ),
                title=item.get(
                    "title",
                    "",
                ),
                description=item.get(
                    "description",
                    "",
                ),
                related_objective_ids=item.get(
                    "related_objective_ids",
                    [],
                ),
                state=cls._parse_learning_opportunity_state(
                    item.get(
                        "state",
                        LearningOpportunityState.RECEIVED.value,
                    )
                ),
                related_evidence_ids=item.get(
                    "related_evidence_ids",
                    [],
                ),
                subsequent_evidence_ids=item.get(
                    "subsequent_evidence_ids",
                    [],
                ),
                reflection=item.get(
                    "reflection",
                    "",
                ),
                recorded_by=item.get(
                    "recorded_by",
                    "",
                ),
                recorded_at=item.get(
                    "recorded_at",
                    "",
                ),
            )
            for item in saved_learning_events
        ]

        for event in project.learning_events:
            if not event.learning_event_id:
                event.learning_event_id = str(uuid4())

        saved_demonstrated_strengths = project_data.get(
            "demonstrated_strengths",
            [],
        )

        project.demonstrated_strengths = [
            DemonstratedStrength(
                strength_id=item.get(
                    "strength_id",
                    "",
                ),
                exercise_id=item.get(
                    "exercise_id",
                    "",
                ),
                scope=cls._parse_preparedness_scope(
                    item.get(
                        "scope",
                        PreparednessScope.INDIVIDUAL.value,
                    )
                ),
                subject_id=item.get(
                    "subject_id",
                    "",
                ),
                title=item.get(
                    "title",
                    "",
                ),
                description=item.get(
                    "description",
                    "",
                ),
                related_objective_ids=item.get(
                    "related_objective_ids",
                    [],
                ),
                related_evidence_ids=item.get(
                    "related_evidence_ids",
                    [],
                ),
                identified_by=item.get(
                    "identified_by",
                    "",
                ),
                recorded_at=item.get(
                    "recorded_at",
                    "",
                ),
            )
            for item in saved_demonstrated_strengths
        ]

        for strength in project.demonstrated_strengths:
            if not strength.strength_id:
                strength.strength_id = str(uuid4())

        saved_readiness_decisions = project_data.get(
            "readiness_decisions",
            [],
        )

        project.readiness_decisions = [
            ReadinessDecision(
                decision_id=item.get(
                    "decision_id",
                    "",
                ),
                outcome=cls._parse_readiness_decision_outcome(
                    item.get(
                        "outcome",
                        ReadinessDecisionOutcome.NOT_ASSESSED.value,
                    )
                ),
                assessment_ids=item.get(
                    "assessment_ids",
                    [],
                ),
                rationale=item.get(
                    "rationale",
                    "",
                ),
                limitations=item.get(
                    "limitations",
                    "",
                ),
                required_action=item.get(
                    "required_action",
                    "",
                ),
                decision_maker=item.get(
                    "decision_maker",
                    "",
                ),
                decision_authority=item.get(
                    "decision_authority",
                    "",
                ),
                recorded_at=item.get(
                    "recorded_at",
                    "",
                ),
                exception_reason=cls._parse_assessment_exception_reason(
                    item.get("exception_reason")
                ),
                exception_explanation=item.get(
                    "exception_explanation",
                    "",
                ),
            )
            for item in saved_readiness_decisions
        ]

        for decision in project.readiness_decisions:
            if not decision.decision_id:
                decision.decision_id = str(uuid4())

        saved_injects = project_data.get(
            "injects",
            project_data.get("exercises", []),
        )
        saved_findings = project_data.get(
            "findings",
            [],
        )

        project.findings = [
            Finding(
                finding_id=item.get(
                    "finding_id",
                    "",
                ),
                title=item.get(
                    "title",
                    "",
                ),
                finding_type=cls._parse_finding_type(
                    item.get(
                        "finding_type",
                        FindingType.OBSERVATION.value,
                    )
                ),
                description=item.get(
                    "description",
                    "",
                ),
                related_decision_id=item.get(
                    "related_decision_id",
                    "",
                ),
                related_assessment_ids=item.get(
                    "related_assessment_ids",
                    [],
                ),
                related_evidence_ids=item.get(
                    "related_evidence_ids",
                    [],
                ),
                recorded_by=item.get(
                    "recorded_by",
                    "",
                ),
                recorded_at=item.get(
                    "recorded_at",
                    "",
                ),
            )
            for item in saved_findings
        ]

        for finding in project.findings:
            if not finding.finding_id:
                finding.finding_id = str(uuid4())
        saved_recommendations = project_data.get(
            "recommendations",
            [],
        )

        project.recommendations = [
            Recommendation(
                recommendation_id=item.get(
                    "recommendation_id",
                    "",
                ),
                title=item.get(
                    "title",
                    "",
                ),
                recommendation_type=cls._parse_recommendation_type(
                    item.get(
                        "recommendation_type",
                        RecommendationType.IMPROVEMENT.value,
                    )
                ),
                description=item.get(
                    "description",
                    "",
                ),
                related_finding_ids=item.get(
                    "related_finding_ids",
                    [],
                ),
                disposition=cls._parse_recommendation_disposition(
                    item.get(
                        "disposition",
                        RecommendationDisposition.NOT_REVIEWED.value,
                    )
                ),
                disposition_rationale=item.get(
                    "disposition_rationale",
                    "",
                ),
                disposition_by=item.get(
                    "disposition_by",
                    "",
                ),
                disposition_authority=item.get(
                    "disposition_authority",
                    "",
                ),
                disposition_at=item.get(
                    "disposition_at",
                    "",
                ),
                recommended_by=item.get(
                    "recommended_by",
                    "",
                ),
                recorded_at=item.get(
                    "recorded_at",
                    "",
                ),
            )
            for item in saved_recommendations
        ]

        for recommendation in project.recommendations:
            if not recommendation.recommendation_id:
                recommendation.recommendation_id = str(uuid4())

        project.injects = [
            Inject(
                number=item.get("number", 0),
                title=item.get("title", ""),
                exercise_time=item.get(
                    "exercise_time",
                    "",
                ),
                phase=item.get("phase", ""),
                source=item.get("source", ""),
                method=item.get("method", ""),
                audience=item.get("audience", ""),
                category=item.get("category", ""),
                inject_text=item.get(
                    "inject_text",
                    "",
                ),
                expected_action=item.get(
                    "expected_action",
                    "",
                ),
                facilitator_notes=item.get(
                    "facilitator_notes",
                    "",
                ),
                attachments=item.get(
                    "attachments",
                    [],
                ),
                status=cls._parse_status(
                    item.get(
                        "status",
                        InjectStatus.PLANNED.value,
                    )
                ),
            )
            for item in saved_injects
        ]

        return project

        saved_evidence_records = project_data.get(
            "evidence_records",
            [],
        )


        # Evidence records are loaded after the project is reconstructed.
        # The evidence block above is now handled in the main load flow,
        # so this legacy lookup should stay out of the class-level parsing
        # section and is not required for the load method to return.

    @staticmethod
    def _parse_assessment_outcome(value):
        for outcome in AssessmentOutcome:
            if outcome.value == value:
                return outcome

        return AssessmentOutcome.NOT_ASSESSED
    @staticmethod
    def _parse_design_trace_event_type(value):
        for event_type in DesignTraceEventType:
            if event_type.value == value:
                return event_type

        return DesignTraceEventType.ATTENTION_IDENTIFIED
    @staticmethod
    def _parse_readiness_decision_outcome(value):
        for outcome in ReadinessDecisionOutcome:
            if outcome.value == value:
                return outcome

        return ReadinessDecisionOutcome.NOT_ASSESSED

    @staticmethod
    def _parse_assessment_exception_reason(value):
        if not value:
            return None

        for reason in AssessmentExceptionReason:
            if reason.value == value:
                return reason

        return AssessmentExceptionReason.OTHER
    
    @staticmethod
    def _parse_preparedness_scope(value):
        for scope in PreparednessScope:
            if scope.value == value:
                return scope

        return PreparednessScope.INDIVIDUAL

    @staticmethod
    def _parse_confidence_stage(value):
        for stage in ConfidenceStage:
            if stage.value == value:
                return stage

        return ConfidenceStage.PRE_EXERCISE

    @staticmethod
    def _parse_learning_opportunity_state(value):
        for state in LearningOpportunityState:
            if state.value == value:
                return state

        return LearningOpportunityState.RECEIVED
    
    @staticmethod
    def _parse_evidence_type(value):
        for evidence_type in EvidenceType:
            if evidence_type.value == value:
                return evidence_type

        return EvidenceType.OTHER

    @staticmethod
    def _parse_finding_type(value):
        for finding_type in FindingType:
            if finding_type.value == value:
                return finding_type

        return FindingType.OTHER
    @staticmethod
    def _parse_recommendation_type(value):
        for recommendation_type in RecommendationType:
            if recommendation_type.value == value:
                return recommendation_type

        return RecommendationType.OTHER

    @staticmethod
    def _parse_recommendation_disposition(value):
        for disposition in RecommendationDisposition:
            if disposition.value == value:
                return disposition

        return RecommendationDisposition.NOT_REVIEWED

    @staticmethod
    def _parse_planned_activity_source_type(value):
        for source_type in PlannedActivitySourceType:
            if source_type.value == value:
                return source_type

        return PlannedActivitySourceType.OTHER

    @staticmethod
    def _parse_action_priority(value):
        for priority in ActionPriority:
            if priority.value == value:
                return priority

        return ActionPriority.MEDIUM

    @staticmethod
    def _parse_action_status(value):
        for status in ActionStatus:
            if status.value == value:
                return status

        return ActionStatus.NOT_STARTED

    @staticmethod
    def _parse_verification_outcome(value):
        for outcome in VerificationOutcome:
            if outcome.value == value:
                return outcome

        return VerificationOutcome.INSUFFICIENT_EVIDENCE

    @staticmethod
    def _parse_training_opportunity_status(value):
        for status in TrainingOpportunityStatus:
            if status.value == value:
                return status

        return TrainingOpportunityStatus.POTENTIAL

    @staticmethod
    def _parse_opportunity_source_type(value):
        for source_type in OpportunitySourceType:
            if source_type.value == value:
                return source_type

        return OpportunitySourceType.OTHER

    @staticmethod
    def _parse_candidate_status(value):
        for status in CandidateStatus:
            if status.value == value:
                return status

        return CandidateStatus.DISCOVERED

    @staticmethod
    def _parse_status(value):
        for status in InjectStatus:
            if status.value == value:
                return status

        return InjectStatus.PLANNED

    @staticmethod
    def _parse_planning_source_type(value):
        for source_type in PlanningSourceType:
            if source_type.value == value:
                return source_type

        return PlanningSourceType.OTHER

    @staticmethod
    def _parse_observation_type(value):
        for observation_type in ObservationType:
            if observation_type.value == value:
                return observation_type

        return ObservationType.OBSERVATION

    @staticmethod
    def _parse_observation_status(value):
        for status in ObservationStatus:
            if status.value == value:
                return status

        return ObservationStatus.DRAFT

    @staticmethod
    def _parse_planning_source_status(value):
        for status in PlanningSourceStatus:
            if status.value == value:
                return status

        return PlanningSourceStatus.PROPOSED
