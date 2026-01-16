from contextlib import asynccontextmanager
from fastapi import Request, Form, APIRouter, FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from settings import SungJukDB_NAME, templates
import aiosqlite

from db import init_db
from routers.member import router as router_member
from routers.board import router as router_board
from routers.sungjuk import router as router_sungjuk

@asynccontextmanager
async def lifespan(app: FastAPI):
    # db.py 파일에 정의된 테이블 생성 함수 실행
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router_member)
app.include_router(router_board)
app.include_router(router_sungjuk)


@app.get("/", response_class=HTMLResponse)
def index():
    # 링크 주소를 라우터 설정에 맞게 변경했습니다.
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
        <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width," initial-scale=1">
    <title>FastAPI 회원/게시판/성적처리 앱</title>
</head>
<body>
    <h1>FastAPI 회원/게시판/성적처리 앱</h1>
    <ul>
        <li><a href="/member/list">회원정보</a></li>
        <li><a href="/board/list">게시판 목록</a></li>
        <li><a href="/sungjuk/list">성적 목록</a></li>
    </ul>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("05bRouter_FastAPI:app", host="0.0.0.0", port=8000, reload=True)