from dataclasses import dataclass
from typing import List, Optional

from helix_personmatching.logics.rule_score import RuleScore


@dataclass
class MatchScoreWithoutThreshold:
    id_source: Optional[str]
    id_target: Optional[str]
    rule_scores: List[RuleScore]
    total_score: float
