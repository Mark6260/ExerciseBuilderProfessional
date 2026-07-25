from dataclasses import dataclass


@dataclass
class DoctrineReference:
    """
    Represents a single piece of doctrine that supports
    the design of an exercise.
    """

    title: str

    reference: str = ""

    version: str = ""

    organisation: str = ""

    description: str = ""

    location: str = ""