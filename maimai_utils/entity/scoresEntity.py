from dataclasses import dataclass


@dataclass
class ScoresEntity:
    music_id: int
    difficulty: int
    tap_miss: int = 0
    tap_goods: int = 0
    tap_greats: int = 0
    tap_perfect: int = 0
    tap_critical_perfect: int = 0
    hold_miss: int = 0
    hold_goods: int = 0
    hold_greats: int = 0
    hold_perfect: int = 0
    hold_critical_perfect: int = 0
    slide_miss: int = 0
    slide_goods: int = 0
    slide_greats: int = 0
    slide_perfect: int = 0
    break_miss: int = 0
    break_goods: int = 0
    break_greats_low: int = 0
    break_greats_medium: int = 0
    break_greats_high: int = 0
    break_perfect_low: int = 0
    break_perfect_medium: int = 0
    break_critical_perfect: int = 0
    
