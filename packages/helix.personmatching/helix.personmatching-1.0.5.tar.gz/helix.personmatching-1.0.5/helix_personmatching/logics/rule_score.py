from dataclasses import dataclass
from typing import List

from helix_personmatching.logics.rule_attribute_score import RuleAttributeScore


@dataclass
class RuleScore:
    id_source: str
    id_target: str
    rule_name: str
    rule_description: str
    rule_score: float
    attribute_scores: List[RuleAttributeScore]
