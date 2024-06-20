import json
import os
import re
import xml.etree.ElementTree as et
from maimai_utils.entity.chartsEntity import SongEntity, ChartEntity


def parse_music_xml(xml_file_path: str) -> SongEntity:
    tree = et.parse(xml_file_path)
    root = tree.getroot()

    music_id = int(root.find('name/id').text)
    music_name = root.find('name/str').text
    bpm = int(root.find('bpm').text)
    sort_name = root.find('sortName').text
    artist_id = int(root.find('artistName/id').text)
    artist_name = root.find('artistName/str').text
    genre_id = int(root.find('genreName/id').text)
    genre_name = root.find('genreName/str').text
    movie_id = int(root.find('movieName/id').text)
    movie_name = root.find('movieName/str').text
    version = int(root.find('version').text)
    add_version_id = int(root.find('AddVersion/id').text)
    add_version_name = root.find('AddVersion/str').text
    release_id = int(root.find('releaseTagName/id').text)
    release_name = root.find('releaseTagName/str').text

    charts = []
    for notes in root.find('notesData'):
        file_name = notes.find('file/path').text
        level = int(notes.find('level').text)
        level_decimal = int(notes.find('levelDecimal').text)
        notes_designer_id = int(notes.find('notesDesigner/id').text)
        notes_designer_name = notes.find('notesDesigner/str').text
        notes_type = int(notes.find('notesType').text)
        music_level_id = int(notes.find('musicLevelID').text)
        max_notes = int(notes.find('maxNotes').text)
        is_enabled = notes.find('isEnable').text.lower() == 'true'

        # 解析ma2文件
        # 解析ma2文件
        ma2_file_path = os.path.join(os.path.dirname(xml_file_path), file_name)
        res = parse_ma2_file(ma2_file_path)

        chart = ChartEntity(
            level=level,
            level_decimal=level_decimal,
            notes_designer_id=notes_designer_id,
            notes_designer_name=notes_designer_name,
            notes_type=notes_type,
            music_level_id=music_level_id,
            max_notes=max_notes,
            is_enabled=is_enabled,
            tap_num=res.get("tap_num", 0),
            hold_num=res.get("hold_num", 0),
            slide_num=res.get("slide_num", 0),
            touch_num=res.get("touch_num", 0),
            touch_hold_num=res.get("touch_hold_num", 0),
            break_num=res.get("break_num", 0),
            all_num=res.get("all_num", 0)
        )
        charts.append(chart)

    song_data = SongEntity(
        music_id=music_id,
        music_name=music_name,
        bpm=bpm,
        sort_name=sort_name,
        artist_id=artist_id,
        artist_name=artist_name,
        genre_id=genre_id,
        genre_name=genre_name,
        movie_id=movie_id,
        movie_name=movie_name,
        version=version,
        add_version_id=add_version_id,
        add_version_name=add_version_name,
        release_id=release_id,
        release_name=release_name,
        charts=charts
    )

    return song_data


def parse_ma2_file(file_path):
    # 初始化一个字典来存储结果，默认值为0
    results = {
        "tap_num": 0,
        "hold_num": 0,
        "slide_num": 0,
        "touch_num": 0,
        "touch_hold_num": 0,
        "break_num": 0,
        "all_num": 0
    }

    # 初始化一个临时字典来存储所有提取的键值对
    temp_results = {
        "T_NUM_TAP": 0,
        "T_REC_TTP": 0,
        "T_NUM_HLD": 0,
        "T_NUM_SLD": 0,
        "T_REC_THO": 0,
        "T_NUM_BRK": 0,
        "T_NUM_ALL": 0
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # 分割每一行
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    key, value = parts
                    if key in temp_results:
                        temp_results[key] = int(value)
    except FileNotFoundError:
        print(f"File {file_path} not found, skipping.")

    # 根据提取到的临时结果计算最终结果
    results["tap_num"] = temp_results.get("T_NUM_TAP", 0) - temp_results.get("T_REC_TTP", 0)
    results["hold_num"] = temp_results.get("T_NUM_HLD", 0)
    results["slide_num"] = temp_results.get("T_NUM_SLD", 0) - temp_results.get("T_REC_THO", 0)
    results["touch_num"] = temp_results.get("T_REC_TTP", 0)
    results["touch_hold_num"] = temp_results.get("T_REC_THO", 0)
    results["break_num"] = temp_results.get("T_NUM_BRK", 0)
    results["all_num"] = temp_results.get("T_NUM_ALL", 0)

    return results


def get_charts_json(streaming_assests_path: str):
    items = os.listdir(streaming_assests_path)
    opt_dirs = list()
    song_data_list = []

    for item in items:
        if bool(re.match(r'^A\d{3}$', item)):
            opt_dirs.append(item)

    for opt_dir in opt_dirs:
        opt_dir_path = os.path.join(streaming_assests_path, opt_dir)
        # 检查是否存在music文件夹
        music_dir_path = os.path.join(opt_dir_path, "music")
        if os.path.isdir(music_dir_path):
            # 获取music文件夹中的所有子文件夹
            music_subdirs = [d for d in os.listdir(music_dir_path) if os.path.isdir(os.path.join(music_dir_path, d))]

            # 打印或处理这些子文件夹
            for subdir in music_subdirs:
                subdir_path = os.path.join(music_dir_path, subdir)
                music_xml_path = os.path.join(subdir_path, "Music.xml")

                # 检查Music.xml文件是否存在
                if os.path.isfile(music_xml_path):
                    print(f"Found Music.xml in {subdir_path}")
                    # 读取并解析Music.xml文件
                    try:
                        song_data = parse_music_xml(music_xml_path)
                        song_data_list.append(song_data)
                    except et.ParseError as e:
                        print(f"Error parsing XML file {music_xml_path}: {e}")
                else:
                    print(f"Music.xml not found in {subdir_path}, skipping.")

    # 将song_data_list转换为JSON并保存到文件
    with open('song_data.json', 'w', encoding='utf-8') as f:
        json.dump([song.to_dict() for song in song_data_list], f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # path = "X:\YOUR\PATH\StreamingAssets"
    path = r"H:\SDGB140\App\Package\Sinmai_Data\StreamingAssets"
    get_charts_json(path)
