from pypinyin import lazy_pinyin, Style
from snownlp import SnowNLP
from datetime import datetime, timezone

# 情感分析结果函数
def score_label(score):
    if score >= 0.6:
        return "偏积极"
    elif score <= 0.4:
        return "偏消极"
    else:
        return "中性"

def get_result(text):
    score = round(SnowNLP(text).sentiments, 2)
    result = {
        "text": text,
        "score": score,
        "label": score_label(score),
        "pinyin": " ".join(lazy_pinyin(text, style=Style.TONE3)),
        "created_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    return result

