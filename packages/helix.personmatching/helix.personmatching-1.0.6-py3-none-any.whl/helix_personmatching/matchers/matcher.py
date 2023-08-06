from typing import List, Union

# noinspection PyPackageRequirements
from fhir.resources.bundle import Bundle

# noinspection PyPackageRequirements
from fhir.resources.patient import Patient

# noinspection PyPackageRequirements
from fhir.resources.person import Person

from helix_personmatching.fhir_manager.fhir_loader import FhirLoader
from helix_personmatching.fhir_manager.fhir_to_dict_manager.fhir_to_dict_manager import (
    FhirToAttributeDict,
)
from helix_personmatching.logics.match_score import MatchScore
from helix_personmatching.logics.match_score_without_threshold import (
    MatchScoreWithoutThreshold,
)
from helix_personmatching.logics.rules_generator import RulesGenerator
from helix_personmatching.logics.score_calculator import ScoreCalculator
from helix_personmatching.logics.scoring_input import ScoringInput
from helix_personmatching.models.rule import Rule


class Matcher:
    # noinspection PyMethodMayBeStatic
    def score_inputs(
        self, *, source: List[ScoringInput], target: List[ScoringInput]
    ) -> List[MatchScoreWithoutThreshold]:
        assert source
        assert target
        rules: List[Rule] = RulesGenerator.generate_rules()

        result: List[MatchScoreWithoutThreshold] = []

        for source_resource in source:
            for target_resource in target:
                result.append(
                    ScoreCalculator.calculate_total_score(
                        rules=rules, source=source_resource, target=target_resource
                    )
                )
        return result

    def match_scoring_inputs(
        self,
        *,
        source: List[ScoringInput],
        target: List[ScoringInput],
        threshold: float = 80.0,
        verbose: bool = False,
    ) -> List[MatchScore]:
        assert source
        assert isinstance(source, list)
        assert target
        assert isinstance(target, list)

        return [
            MatchScore(
                id_source=score.id_source,
                id_target=score.id_target,
                rule_scores=score.rule_scores if verbose else [],
                total_score=score.total_score,
                threshold=threshold,
                matched=(score.total_score >= threshold),
            )
            for score in self.score_inputs(source=source, target=target)
        ]

    def match(
        self,
        *,
        source_json: Union[str, List[str]],
        target_json: Union[str, List[str]],
        threshold: float = 80.0,
        verbose: bool = False,
    ) -> List[MatchScore]:
        assert source_json
        assert isinstance(source_json, str) or isinstance(source_json, list)
        assert target_json
        assert isinstance(target_json, str) or isinstance(target_json, list)

        source: List[ScoringInput] = FhirLoader.get_scoring_inputs(
            resource_json=source_json
        )
        target: List[ScoringInput] = FhirLoader.get_scoring_inputs(
            resource_json=target_json
        )
        match_score: List[MatchScore] = self.match_scoring_inputs(
            source=source, target=target, threshold=threshold, verbose=verbose
        )
        return match_score

    def match_resources(
        self,
        *,
        source: Union[Patient, Person, Bundle],
        target: Union[Patient, Person, Bundle],
        threshold: float = 80.0,
        verbose: bool = False,
    ) -> List[MatchScore]:
        source_scoring_inputs: List[
            ScoringInput
        ] = FhirToAttributeDict.get_scoring_inputs_for_resource(resource=source)
        target_scoring_inputs: List[
            ScoringInput
        ] = FhirToAttributeDict.get_scoring_inputs_for_resource(resource=target)
        return self.match_scoring_inputs(
            source=source_scoring_inputs,
            target=target_scoring_inputs,
            threshold=threshold,
            verbose=verbose,
        )
