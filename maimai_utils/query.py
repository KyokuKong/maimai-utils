import json
import importlib.resources as pkg_resources
from maimai_utils.entity.chartsEntity import SongData, ChartData


def load_song_data_from_json():
    def chart_data_from_dict(data):
        return ChartData(**data)

    def song_data_from_dict(data):
        charts = [chart_data_from_dict(chart) for chart in data['charts']]
        return SongData(
            music_id=data['music_id'],
            music_name=data['music_name'],
            bpm=data['bpm'],
            sort_name=data['sort_name'],
            artist_id=data['artist_id'],
            artist_name=data['artist_name'],
            genre_id=data['genre_id'],
            genre_name=data['genre_name'],
            movie_id=data['movie_id'],
            movie_name=data['movie_name'],
            version=data['version'],
            add_version_id=data['add_version_id'],
            add_version_name=data['add_version_name'],
            release_id=data['release_id'],
            release_name=data['release_name'],
            charts=charts
        )

    with pkg_resources.open_text('maimai_utils.data', 'song_data.json') as f:
        data_list = json.load(f)
        song_data_list = [song_data_from_dict(data) for data in data_list]
    return song_data_list


class MaiQuery:
    def __init__(self):
        self.song_data = load_song_data_from_json()

    def find_song_by_music_id(self, music_id):
        for song in self.song_data:
            if song.music_id == music_id:
                return song
        return None

    def find_songs_by_level(self, level_decimal):
        integer_part = int(level_decimal)
        decimal_part = int((level_decimal - integer_part) * 10)
        matching_songs = []

        for song in self.song_data:
            for chart in song.charts:
                if chart.level == integer_part and chart.level_decimal == decimal_part:
                    matching_songs.append(song)
                    break

        return matching_songs


maiquery = MaiQuery()
