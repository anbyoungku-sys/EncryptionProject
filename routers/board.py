# board.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from settings import BoardDB_NAME, templates
from fastapi.templating import Jinja2Templates
import aiosqlite

# 메인에서 사용할 라우터 객체 생성 (prefix="/board" 이므로 이 파일의 모든 URL 앞에 /board가 자동으로 붙음)
router = APIRouter(prefix="/board", tags=["board"])

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# DB 파일 경로
BoardDB_NAME = "board.db"

#-----------------------------------------------------------
# 게시판 목록 조회
# 실제 접속 주소: /board/list
#-----------------------------------------------------------
@router.get("/list", response_class=HTMLResponse)
async def board_list(request: Request):
    async with aiosqlite.connect(BoardDB_NAME) as db:
        async with db.execute("SELECT bdno, title, username, regdate, views FROM board ORDER BY bdno DESC") as cur:
            results = await cur.fetchall()

    boards = []
    for rs in results:
        boards.append({
            "bdno": rs[0], "title": rs[1], "username": rs[2],
            "regdate": rs[3][:10], "views": rs[4]
        })

    # 파일 구조상 templates/board/board_list.html
    return templates.TemplateResponse("board/board_list.html", {"request": request, "boards": boards})

#-----------------------------------------------------------
# 게시글 작성 폼
# 실제 접속 주소: /board/new
#-----------------------------------------------------------
@router.get("/new", response_class=HTMLResponse)
def board_new_form(request: Request):
    return templates.TemplateResponse("board/board_new.html", {"request": request})

#-----------------------------------------------------------
# 게시글 작성 처리
#-----------------------------------------------------------
@router.post("/new")
async def board_new(title: str = Form(...), username: str = Form(...), contents: str = Form(...)):
    async with aiosqlite.connect(BoardDB_NAME) as db:
        await db.execute("INSERT INTO board (title, username, contents) VALUES (?, ?, ?)",
                         (title, username, contents))
        await db.commit()

    # 작성 완료 후 목록으로 이동 (전체 경로 입력)
    return RedirectResponse(url="/board/list", status_code=303)

#-----------------------------------------------------------
# 게시글 본문 조회
# 실제 접속 주소: /board/{bdno}
#-----------------------------------------------------------
@router.get("/{bdno}", response_class=HTMLResponse)
async def board_detail(request: Request, bdno: int):
    async with aiosqlite.connect(BoardDB_NAME) as db:
        await db.execute("UPDATE board SET views = views + 1 WHERE bdno = ?", (bdno,))
        await db.commit()

        async with db.execute("SELECT * FROM board WHERE bdno = ?", (bdno,)) as cur:
            result = await cur.fetchone()

    if result is None:
        return HTMLResponse("해당 글이 존재하지 않습니다.", status_code=404)

    board = {"bdno": result[0], "title": result[1], "username": result[2],
             "regdate": result[3], "views": result[4], "contents": result[5]}

    return templates.TemplateResponse("board/board_detail.html", {"request": request, "bd": board})