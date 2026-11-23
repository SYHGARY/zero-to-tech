from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from storage import init_db, save_record, get_history
from business import get_result

# 创建FastAPI对象，并设置通行的URL与方法
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
)

init_db()  # 初始化数据库

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

# 定义接收的文字对象（字符串）
class AnalyzeRequest(BaseModel):
    text: str

# 首页页面路由
@app.get("/api/profile")
def get_profile():
    return profile

# 文字分析页面路由
@app.post("/api/analyze")
def analyze(req: AnalyzeRequest):
    text = req.text
    result = get_result(text)
    save_record(result)
    return result

# 查看历史记录页面路由
@app.get("/api/history")
def history():
    return get_history()

