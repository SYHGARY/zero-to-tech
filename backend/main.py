from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from storage import init_db, save_record, get_history
from business import get_result

import uuid
from fastapi import Request, Response

import os
from dotenv import load_dotenv

load_dotenv()                        # ← 读同目录下的 .env

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS").split(",")

def get_session_id(request: Request, response: Response) -> str:
    sid = request.cookies.get("session_id")      # 先看有没有纸条
    if not sid:                                  # 第一次来，没有则发一张
        sid = uuid.uuid4().hex                   # 生成UUID
        response.set_cookie(
            "session_id", sid,
            httponly=True, samesite="lax",
            max_age=60 * 60 * 24 * 30,            # 记 30 天
        )
    return sid

# 创建FastAPI对象，并设置通行的URL与方法
# 同时允许携带凭证（Cookie)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,          # 允许的源不写死，来自配置
    allow_methods=["GET", "POST"],
    allow_credentials=True,
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
def analyze(req: AnalyzeRequest, request : Request, response : Response):
    sid = get_session_id(request, response)
    text = req.text
    result = get_result(text)
    save_record(sid, result)
    return result

# 查看历史记录页面路由
@app.get("/api/history")
def history(request : Request, response : Response, limit : int = 10):
    sid = get_session_id(request, response)
    return get_history(sid, limit)


