from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from models import Question
from database import engine, init_db
from limiter import is_ip_allowed
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 异步初始化数据库连接
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "https://mht.misaka.cn",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/submit")
async def submit_question(request: Request):
    # 从请求体中异步读取 JSON 数据
    data = await request.json()

    # 获取并去除内容字符串首尾空格（默认为空字符串，防止缺失 key 报错）
    content = data.get("content", "").strip()

    # 校验内容是否为空，或者长度超过 500 字符，违反则返回 400 错误
    if len(content) == 0 or len(content) > 500:
        raise HTTPException(status_code=400, detail="内容必须在 1 到 500 字之间")

    # 获取发起请求的客户端 IP 地址（FastAPI 提供）
    ip = request.client.host
    user_agent = request.headers.get("user-agent", "")

    # 使用 Redis 校验是否允许此 IP 投稿（每小时只允许一次）
    if not await is_ip_allowed(ip, user_agent):
        raise HTTPException(status_code=429, detail="每个 IP 每小时只能投稿一次")

    # 构建一个新的 Question 对象（使用 SQLModel 定义）
    question = Question(content=content, ip=ip)

    # # 使用 SQLModel 提供的 Session 会话机制操作数据库
    with Session(engine) as session:
        session.add(question)   # 添加记录
        session.commit()        # 提交事务（插入数据）

    # 返回成功响应（JSON）
    return {"status": "提交成功"}
