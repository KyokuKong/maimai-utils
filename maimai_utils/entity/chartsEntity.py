from dataclasses import dataclass, asdict


@dataclass
class ChartEntity:
    level: int
    level_decimal: int
    notes_designer_id: int
    notes_designer_name: str
    notes_type: int
    music_level_id: int
    max_notes: int
    is_enabled: bool
    tap_num: int
    hold_num: int
    slide_num: int
    touch_num: int
    touch_hold_num: int
    break_num: int
    all_num: int

    def to_dict(self):
        return asdict(self)


@dataclass
class SongEntity:
    """
    存储谱面数据时使用的数据类
    """
    music_id: int
    music_name: str
    bpm: int
    sort_name: str
    artist_id: int
    artist_name: str
    genre_id: int
    genre_name: str
    movie_id: int
    movie_name: str
    version: int
    add_version_id: int
    add_version_name: str
    release_id: int
    release_name: str
    charts: list[ChartEntity]

    def to_dict(self):
        data = asdict(self)
        data['charts'] = [chart.to_dict() for chart in self.charts]
        return data
