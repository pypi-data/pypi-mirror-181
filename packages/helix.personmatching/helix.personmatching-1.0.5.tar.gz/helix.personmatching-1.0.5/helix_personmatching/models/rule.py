from typing import List


class Rule:
    def __init__(
        self,
        name: str,
        description: str,
        number: int,
        attributes: List[str],
        score: float,
    ) -> None:
        self.name: str = name
        self.description: str = description
        self.number: int = number
        self.attributes: List[str] = attributes
        self.score: float = score
