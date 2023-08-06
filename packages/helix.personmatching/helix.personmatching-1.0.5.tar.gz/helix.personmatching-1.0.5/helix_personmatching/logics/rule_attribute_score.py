from dataclasses import dataclass
from typing import Optional


@dataclass
class RuleAttributeScore:
    attribute: str
    score: float
    present: bool
    source: Optional[str]
    target: Optional[str]
