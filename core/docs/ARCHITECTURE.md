# Exercise Director Architecture

## Purpose

Exercise Director is designed to assist instructors, Exercise Directors and organisations
to design, deliver and assure exercises that build operational capability.

The application is based on the principle that software should strengthen and support
professional judgement, never replace it.

---

# Core Philosophy

Exercises do not exist simply to deliver injects.

Exercises exist to build operational capability.

Every element within Exercise Director should therefore contribute to the following
golden thread.

Mission

↓

Capability

↓

Collective Training Objectives (CTOs)

↓

Learning Objectives

↓

Doctrine

↓

Exercise Design

↓

Injects

↓

Assessment

↓

Evidence

↓

Assurance

↓

Operational Readiness

---

# Core Business Objects

## Project

Represents a complete exercise.

Contains:

- Capability
- Doctrine References
- Collective Training Objectives
- Learning Objectives
- Injects
- Assessments
- Assurance

---

## Capability

Defines the operational capability the exercise is designed to develop.

Examples:

- Conduct Obstacle Crossing
- Coordinate National Flood Response
- Conduct Joint Fires
- Restore National Power Infrastructure

---

## Collective Training Objectives (CTOs)

Describe the collective tasks required to build capability.

Each CTO is supported by one or more learning objectives.

---

## Learning Objectives

Describe what individuals or teams should demonstrate.

Every learning objective should:

- support a CTO
- be supported by doctrine
- be assessed by one or more injects

---

## Doctrine References

Provide the authoritative basis for training.

Doctrine answers:

Why are we training this?

---

## Injects

Provide opportunities for learners to demonstrate performance.

Injects are evidence opportunities.

They are not training objectives.

---

## Assessment Records

Capture instructor observations.

Assessment produces evidence.

Evidence supports assurance.

---

## Assurance

Provides confidence that:

- objectives are covered
- doctrine is current
- assessments exist
- evidence supports conclusions

Assurance is the final product of exercise design.

---

# Design Principles

Mission before mechanics.

Capability before activity.

Doctrine with purpose.

Evidence before opinion.

People before software.

Professional judgement remains central.

Every exercise should improve organisational learning.

---

# Development Principles

One brick.

One test.

One commit.

Small changes.

Clean architecture.

Continuous improvement.

---

Better prepared today.

Stronger tomorrow.
## Architecture History

Version 0.1

- Initial architecture defined.
- Capability introduced.
- Doctrine linked to objectives.
- Assessment business object introduced.