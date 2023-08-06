import dataclasses
import json
from pathlib import Path
from typing import List

from helix_personmatching.logics.match_score import MatchScore
from helix_personmatching.matchers.matcher import Matcher


def test_hapi_partial_match() -> None:
    data_dir: Path = Path(__file__).parent.joinpath("./person_data")

    with open(data_dir.joinpath("bwell_master_person.json")) as file:
        bwell_master_person_json = file.read()

    with open(data_dir.joinpath("hapi_person.json")) as file:
        hapi_person_json = file.read()

    matcher = Matcher()

    scores: List[MatchScore] = matcher.match(
        source_json=hapi_person_json,
        target_json=bwell_master_person_json,
        verbose=True,
    )

    assert len(scores) == 1
    score = scores[0]

    print(f"\r\nscore.matched: {score.matched}")
    assert score.matched is False

    print(f"\r\nscore.total_score: {score.total_score}")
    assert score.total_score == 77.52976190476191

    score_dict = dataclasses.asdict(score)

    scores_json = json.dumps(score_dict, default=str)
    print(scores_json)

    with open(data_dir.joinpath("expected_scores.json")) as file:
        expected_scores = json.loads(file.read())

    assert score_dict == expected_scores
