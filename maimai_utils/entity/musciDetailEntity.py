from dataclasses import dataclass
from maimai_utils.entity.scoresEntity import ScoresEntity


@dataclass
class MusicDetailEntity:
    acc: int
    dx_score: int
    max_combo: int
    total_combo: int
    combo_type: int
    sync_type: int
    score_rank: int
    score_result: ScoresEntity
