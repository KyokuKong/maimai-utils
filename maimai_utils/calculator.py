import random
from tkinter import N, NO
from maimai_utils.entity.musciDetailEntity import MusicDetailEntity
from maimai_utils.query import maiquery
from maimai_utils.entity import ScoresEntity


def get_score_rank(acc: float | int):
    print(acc)
    if acc >= 1.01 and acc < 1.02:
        acc = acc * 1000000
        
    if acc >= 1005000:
        return 13
    elif acc >= 1000000:
        return 12
    elif acc >= 995000:
        return 11
    elif acc >= 990000:
        return 10
    elif acc >= 980000:
        return 9
    elif acc >= 970000:
        return 8
    elif acc >= 940000:
        return 7
    elif acc >= 900000:
        return 6
    elif acc >= 800000:
        return 5
    elif acc >= 750000:
        return 4
    elif acc >= 700000:
        return 3
    elif acc >= 600000:
        return 2
    elif acc >= 500000:
        return 1
    else:
        return 0


def calc_score(scores: ScoresEntity):
    """自动从输入的成绩对象中读取并生成数据，计算出对应的分数
    计算的分数包含准确度（ACC）和DX分数，并且会自动生成成绩的各种flag

    Args:
        scores (ScoresEntity): 成绩对象

    Returns:
        _type_: 计算后的乐曲信息对象
    """
    # 通过减法运算得出总权重并运算获得ACC
    # 获取对应谱面的完整音符数量
    res = maiquery.find_chart_by_music_id_and_difficulty(scores.music_id, scores.difficulty)
    if res:
        # 获得谱面对应的数据
        max_tap = res.tap_num + res.touch_num
        max_hold = res.hold_num + res.touch_hold_num
        max_slide = res.slide_num
        max_break = res.break_num
        # 按权重比计算出总权重
        max_weight = max_tap + max_hold * 2 + max_slide * 3 + max_break * 5
        # 计算实际数据的总权重
        fact_tap = max_tap - scores.tap_miss - scores.tap_goods * 0.5 - scores.tap_greats * 0.2
        fact_hold = max_hold - scores.hold_miss - scores.hold_goods * 0.5 - scores.hold_greats * 0.2
        fact_slide = max_slide - scores.slide_miss - scores.slide_goods * 0.5 - scores.slide_greats * 0.2
        fact_break = max_break - scores.break_miss - scores.break_goods * 0.6 - scores.break_greats_low * 0.5 - scores.break_greats_medium * 0.4 - scores.break_greats_high * 0.2
        fact_weight = fact_tap + fact_hold * 2 + fact_slide * 3 + fact_break * 5
        # 得到基础分准确度比例
        base_acc = fact_weight / max_weight
        # 计算额外分数
        max_extra = max_break
        fact_extra = max_break - scores.break_miss - scores.break_goods * 0.7 - (scores.break_greats_low + scores.break_greats_medium + scores.break_greats_high) * 0.6 - scores.break_perfect_low * 0.5 - scores.break_perfect_medium * 0.25
        extra_acc = fact_extra / max_extra
        # 得到总分
        full_acc: int = int((base_acc + extra_acc / 100) * 1000000)
        
        # 计算DX分数
        # DX分数的计算方式是：CRITICAL PERFECT判定取得3分，PERFECT判定取得2分，GREAT判定取得1分
        tap_dx_score = scores.tap_critical_perfect * 3 + scores.tap_perfect * 2 + scores.tap_greats
        hold_dx_score = scores.hold_critical_perfect * 3 + scores.hold_perfect * 2 + scores.hold_greats
        slide_dx_score = scores.slide_perfect * 3 + scores.slide_greats
        break_dx_score = scores.break_critical_perfect * 3 + (scores.break_perfect_medium + scores.break_perfect_low) * 2 + scores.break_greats_medium + scores.break_greats_low + scores.break_greats_high
        # 总分
        dx_score = tap_dx_score + hold_dx_score + slide_dx_score + break_dx_score
        return full_acc, dx_score


def new_score(
    music_id: int,
    difficulty: int,
    tap_miss: int = 0,
    tap_goods: int = 0,
    tap_greats: int = 0,
    tap_perfect: int = 0,
    tap_critical_perfect: int = 0,
    hold_miss: int = 0,
    hold_goods: int = 0,
    hold_greats: int = 0,
    hold_perfect: int = 0,
    hold_critical_perfect: int = 0,
    slide_miss: int = 0,
    slide_goods: int = 0,
    slide_greats: int = 0,
    slide_perfect: int = 0,
    break_miss: int = 0,
    break_goods: int = 0,
    break_greats_low: int = 0,
    break_greats_medium: int = 0,
    break_greats_high: int = 0,
    break_perfect_low: int = 0,
    break_perfect_medium: int = 0,
    break_critical_perfect: int = 0
):
    """用于新建一个成绩对象，可以只传入必要的参数，但是大概率会导致DX分数计算结果不准确

    Returns:
        _type_: ScoresEntity对象
    """
    return ScoresEntity(
        music_id,
        difficulty,
        tap_miss,
        tap_goods,
        tap_greats,
        tap_perfect,
        tap_critical_perfect,
        hold_miss,
        hold_goods,
        hold_greats,
        hold_perfect,
        hold_critical_perfect,
        slide_miss,
        slide_goods,
        slide_greats,
        slide_perfect,
        break_miss,
        break_goods,
        break_greats_low,
        break_greats_medium,
        break_greats_high,
        break_perfect_low,
        break_perfect_medium,
        break_critical_perfect)


def new_all_perfect_score(music_id, difficulty):
    """随机生成一个AP成绩对象"""
    # 拉取歌曲信息
    res = maiquery.find_chart_by_music_id_and_difficulty(music_id, difficulty)
    if res:
        # 得到总其他音符数量和总break数量
        all_tap = res.tap_num + res.touch_num
        all_hold = res.hold_num + res.touch_hold_num
        all_slide = res.slide_num
        all_break = res.break_num
        # 随机生成一个0.5-1.0之间的数值作为大p率
        very_perfect_rate = random.uniform(0.6, 0.9)
        # 计算对应音符的大p数量
        very_perfect_tap = int(all_tap * very_perfect_rate)
        very_perfect_hold = int(all_hold * very_perfect_rate)
        very_perfect_slide = int(all_slide * very_perfect_rate)
        very_perfect_break = int(all_break * very_perfect_rate)
        # 计算对应音符的小p数量
        perfect_tap = all_tap - very_perfect_tap
        perfect_hold = all_hold - very_perfect_hold
        perfect_slide = all_slide - very_perfect_slide
        perfect_break = all_break - very_perfect_break
        # 按照随机结果生成一个Score
        score =  new_score(
            music_id,
            difficulty,
            tap_perfect=perfect_tap,
            tap_critical_perfect=very_perfect_tap,
            hold_perfect=perfect_hold,
            hold_critical_perfect=very_perfect_hold,
            slide_perfect=perfect_slide,
            break_perfect_medium=perfect_break,
            break_critical_perfect=very_perfect_break
        )
        # 计算分数
        calc_res = calc_score(score)
        if calc_res:
            acc: int = calc_res[0]
            dx_score: int = calc_res[1]
            return MusicDetailEntity(acc, dx_score, res.max_notes, res.max_notes, 3, 0, get_score_rank(acc), score)


def new_empty_score(music_id, difficulty):
    """生成一个成绩数据为空的成绩对象"""
    res = maiquery.find_chart_by_music_id_and_difficulty(music_id, difficulty)
    if res:
        # 得到总其他音符数量和总break数量
        all_tap = res.tap_num + res.touch_num
        all_hold = res.hold_num + res.touch_hold_num
        all_slide = res.slide_num
        all_break = res.break_num
        score =  new_score(
            music_id,
            difficulty,
            tap_miss=all_tap,
            hold_miss=all_hold,
            slide_miss=all_slide,
            break_miss=all_break
        )
        return MusicDetailEntity(0, 0, 0, res.max_notes, 0, 0, 0, score)
        




