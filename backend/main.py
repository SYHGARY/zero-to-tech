from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pypinyin import lazy_pinyin, Style
from snownlp import SnowNLP
import json
from datetime import datetime, timezone

# 创建FastAPI对象，并设置通行的URL与方法
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
)

# 首页的内容数据
profile = {
    "heroTitle": "关于我",
    "heroSubtitle": "项目，创意，灵感，心得，我的作品",
    "featuredWork": {
        "kicker": "作品",
        "title": "文字实验室",
        "copy": "拼音和情绪，挖掘中文里的细节",
        "linkLabel": "打开作品",
    },
    "identity": {
        "motto": "天道酬勤，正道直行",
        "learning": "零到全栈",
    },
}

# 用于存储查询的历史文件
HISTORY_FILE = "history.json"

# 加载历史记录
def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# 向历史文件中添加记录
# 取出所有记录 -> 在记录最后添加一条记录 -> 整个写回
def save_record(record):
    records = load_history()
    records.append(record)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

# 定义接收的文字对象（字符串）
class AnalyzeRequest(BaseModel):
    text: str

# 首页页面路由
@app.get("/api/profile")
def get_profile():
    return profile

# 情感分析结果函数
def score_label(score):
    if score >= 0.6:
        return "偏积极"
    elif score <= 0.4:
        return "偏消极"
    else:
        return "中性"

# 文字分析页面路由
@app.post("/api/analyze")
def analyze(req: AnalyzeRequest):
    text = req.text
    score = round(SnowNLP(req.text).sentiments, 2)
    result = {
        "text": text,
        "score": score,
        "label": score_label(score),
        "pinyin": " ".join(lazy_pinyin(text, style=Style.TONE3)),
        "created_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    save_record(result)
    return result

# 查看历史记录页面路由
@app.get("/api/history")
def history():
    records = load_history()   # 读出文件里的全部记录
    records.reverse()          # 将记录倒置，新的排前面
    return records[:10]        # 取最近10条

