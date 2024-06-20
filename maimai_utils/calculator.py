from maimai_utils.query import maiquery
from maimai_utils.entity import ScoresEntity


def calc_acc(scores: ScoresEntity):
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
        full_acc = base_acc + extra_acc / 100
        return full_acc


print(calc_acc(ScoresEntity(11607, 3, tap_greats=5, hold_greats=1, tap_miss=1, break_perfect_medium=7)))
