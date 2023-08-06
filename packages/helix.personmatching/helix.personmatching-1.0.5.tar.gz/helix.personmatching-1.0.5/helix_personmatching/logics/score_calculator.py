from typing import Any, List, Optional, cast

from rapidfuzz import fuzz

from helix_personmatching.logics.match_score_without_threshold import (
    MatchScoreWithoutThreshold,
)
from helix_personmatching.logics.rule_attribute_score import RuleAttributeScore
from helix_personmatching.logics.rule_score import RuleScore
from helix_personmatching.logics.scoring_input import ScoringInput
from helix_personmatching.models.rule import Rule


class ScoreCalculator:
    @staticmethod
    def initialize_score(rules: List[Rule]) -> None:
        for rule in rules:
            rule.score = 0.0

    @staticmethod
    def calculate_total_score(
        rules: List[Rule], source: ScoringInput, target: ScoringInput
    ) -> MatchScoreWithoutThreshold:
        match_results: List[RuleScore] = ScoreCalculator.calculate_score(
            rules=rules, source=source, target=target
        )
        if len(match_results) == 0:
            return MatchScoreWithoutThreshold(
                id_source=source.id_,
                id_target=target.id_,
                rule_scores=match_results,
                total_score=0.0,
            )
        # Get the average match score as "final score" result
        #   w/ high confidence w/ match score >= 80.0
        final_score: float = 0
        for match_result in match_results:
            final_score += cast(float, match_result.rule_score or 0)
        final_score /= len(match_results)
        return MatchScoreWithoutThreshold(
            id_source=source.id_,
            id_target=target.id_,
            rule_scores=match_results,
            total_score=final_score,
        )

    @staticmethod
    def calculate_score(
        rules: List[Rule], source: ScoringInput, target: ScoringInput
    ) -> List[RuleScore]:
        """
        Calculate matching scores for ALL rules between FHIR Person-Person, or Person-Patient, or Person/Patient-AppUser
        :param rules: generated rules by RulesGenerator
        :param source: Dictionary of Pii data for FHIR Person/Patient data, or AppUser data
        :param target: Dictionary of Pii data for FHIR Person/Patient data, or AppUser data
        :return: list of dictionary for rules score results for all rules
        """

        rules_score_results: List[RuleScore] = []

        for rule in rules:
            rule_score_result: Optional[
                RuleScore
            ] = ScoreCalculator.calculate_score_for_rule(rule, source, target)
            if rule_score_result:
                rules_score_results.append(rule_score_result)

        return rules_score_results

    @staticmethod
    def calculate_score_for_rule(
        rule: Rule, source: ScoringInput, target: ScoringInput
    ) -> Optional[RuleScore]:
        """
        Calculate a matching score for one rule between FHIR Person-Person, or Person-Patient, or Person/Patient-AppUser
        :param rule: one rule in the generated rules by RulesGenerator
        :param source: Dictionary of Pii data for FHIR Person/Patient data, or AppUser data
        :param target: Dictionary of Pii data for FHIR Person/Patient data, or AppUser data
        :return: Dictionary of 1 rule score result
        """

        id_data_source: Optional[Any] = source.id_
        id_data_target: Optional[Any] = target.id_
        if not (id_data_source and id_data_target):
            return None

        rule_attribute_scores: List[RuleAttributeScore] = []
        score_avg: float = 0.0
        for attribute in rule.attributes:
            rule_attribute_score: RuleAttributeScore = RuleAttributeScore(
                attribute=attribute, score=0.0, present=False, source=None, target=None
            )
            val_source: Optional[str] = getattr(source, attribute)
            val_target: Optional[str] = getattr(target, attribute)

            if val_source and val_target:
                rule_attribute_score.present = True
                # calculate exact string match on "trimmed lower" string values
                score_for_attribute = fuzz.ratio(
                    str(val_source).strip().lower(), str(val_target).strip().lower()
                )
                score_avg += score_for_attribute
                rule_attribute_score.score = score_for_attribute
                rule_attribute_score.source = val_source
                rule_attribute_score.target = val_target
            rule_attribute_scores.append(rule_attribute_score)

        score_avg /= len(rule.attributes)
        rule.score = score_avg

        rule_score: RuleScore = RuleScore(
            id_source=str(id_data_source),
            id_target=str(id_data_target),
            rule_name=rule.name,
            rule_description=rule.description,
            rule_score=rule.score,
            attribute_scores=rule_attribute_scores,
        )

        return rule_score
