import json
from pathlib import Path

from core.doctrine import DoctrineReference
from core.inject import Inject, InjectStatus
from core.objective import ExerciseObjective
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
from core.improvement.action import (
    ActionPriority,
    ActionStatus,
    ImprovementAction,
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


class Project:
    def __init__(self, name="Untitled Project"):
        self.name = name

        self.operational_requirement = OperationalRequirement()
        self.apprentice_notebook = ApprenticeNotebook()

        self.injects: list[Inject] = []
        self.objectives: list[ExerciseObjective] = []
        self.doctrine_references: list[DoctrineReference] = []
        self.evidence_records: list[EvidenceRecord] = []
        self.assessment_records: list[AssessmentRecord] = []
        self.readiness_decisions: list[ReadinessDecision] = []
        self.findings: list[Finding] = []
        self.recommendations: list[Recommendation] = []
        self.improvement_actions: list[ImprovementAction] = []
        self.training_opportunities: list[TrainingOpportunity] = []
        self.candidate_opportunities: list[CandidateOpportunity] = []

    def add_inject(self, inject: Inject):
        self.injects.append(inject)

    def add_objective(self, objective: ExerciseObjective):
        self.objectives.append(objective)

    def add_doctrine_reference(
        self,
        doctrine_reference: DoctrineReference,
        ):
        self.doctrine_references.append(doctrine_reference)
    def add_evidence(self, evidence: EvidenceRecord):
        self.evidence_records.append(evidence)
    def add_assessment(self, assessment: AssessmentRecord):
        self.assessment_records.append(assessment)

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
    def save(self, filename):
        readiness_gap = self.operational_requirement.readiness.readiness_gap

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
                    "outcome": assessment.outcome.value,
                    "evidence_ids": assessment.evidence_ids,
                    "comments": assessment.comments,
                    "assessor": assessment.assessor,
                    "recorded_at": assessment.recorded_at,
                }
                for assessment in self.assessment_records
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


        saved_evidence_records = project_data.get(
            "evidence_records",
            [],
        )

        return project
    @staticmethod
    def _parse_assessment_outcome(value):
        for outcome in AssessmentOutcome:
            if outcome.value == value:
                return outcome

        return AssessmentOutcome.NOT_ASSESSED

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
