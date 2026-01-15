# 파일명은 04bMemberBoard_FastAPI.py로 작성할 것!
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import aiosqlite
import sqlite3

# DB 하나로 통합 관리하는 것이 효율적이지만, 요청대로 두 개를 유지할 경우를 위해 수정
BoardDB_NAME = "board.db"
MemberDB_NAME = "member.db"

#------------------
#---  DB 테이블  ---
#------------------

#-----------------------------------------------------------
# 앱 시작 시 두 DB의 테이블을 모두 생성
#-----------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with aiosqlite.connect(BoardDB_NAME) as db1:
        await db1.execute("""
              CREATE TABLE IF NOT EXISTS board (
                   bdno INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   username TEXT NOT NULL,
                   regdate TEXT DEFAULT (datetime('now','localtime')),
                  views INTEGER DEFAULT 0,
                  contents TEXT NOT NULL)
              """)
        await db1.commit()

    async with aiosqlite.connect(MemberDB_NAME) as db2:
        await db2.execute("""
              CREATE TABLE IF NOT EXISTS member (
                memberid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                name TEXT,
                email TEXT UNIQUE,
                regdate TEXT DEFAULT (datetime('now','localtime'))
                  )
              """)
        await db2.commit()
    yield

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

#-----------------------------------------------------------
# 루트 경로: 로그인 페이지가 없다는 에러를 방지하기 위해 메뉴 노출
#-----------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    html_content = """
    <h1>FastAPI 서비스 메인</h1>
    <ul>
        <li><a href="/login">로그인</a></li>
        <li><a href="/join">회원가입</a></li>
        <li><a href="/board">게시판 목록</a></li>
    </ul>
    """
    return HTMLResponse(content=html_content)

#------------------
# --- 게시판 기능 ---
#------------------

#-----------------------------------------------------------
# 게시판 목록 조회: DB에서 전체 게시글을 가져와 리스트 형태로 화면에 출력
#-----------------------------------------------------------
@app.get("/board", response_class=HTMLResponse)
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

    return templates.TemplateResponse("board_list.html", {"request": request, "boards": boards})

#-----------------------------------------------------------
# 게시글 작성 폼: 새로운 글을 작성할 수 있는 입력 화면(HTML)을 반환
#-----------------------------------------------------------
@app.get("/board/new", response_class=HTMLResponse)
def board_new_form(request: Request):
    return templates.TemplateResponse("board_new.html", {"request": request})

#-----------------------------------------------------------
# 게시글 작성 처리: 사용자가 입력한 제목, 작성자, 내용을 DB에 저장
#-----------------------------------------------------------
@app.post("/board/new")
async def board_new(title: str = Form(...), username: str = Form(...), contents: str = Form(...)):
    async with aiosqlite.connect(BoardDB_NAME) as db:
        await db.execute("INSERT INTO board (title, username, contents) VALUES (?, ?, ?)",
                         (title, username, contents))
        await db.commit()
    return RedirectResponse(url="/board", status_code=303)

#-----------------------------------------------------------
# 게시글 본문 조회: 특정 번호(bdno)의 글 상세 내용을 보여줌
#-----------------------------------------------------------
@app.get("/board/{bdno}", response_class=HTMLResponse)
async def board_detail(request: Request, bdno: int):
    async with aiosqlite.connect(BoardDB_NAME) as db:
        # 1. 상세 내용을 보기 전 해당 게시글의 조회수(views)를 1 증가시킴
        await db.execute("UPDATE board SET views = views + 1 WHERE bdno = ?", (bdno,))
        await db.commit()

        # 2. 해당 번호의 전체 게시글 정보(제목, 작성자, 날짜, 내용 등)를 조회
        async with db.execute("SELECT * FROM board WHERE bdno = ?", (bdno,)) as cur:
            result = await cur.fetchone()
    # 만약 해당하는 번호의 글이 DB에 없다면 404 에러 메시지 반환
    if result is None: return HTMLResponse("해당 글이 존재하지 않습니다.", status_code=404)
    board = {"bdno": result[0], "title": result[1], "username": result[2],
             "regdate": result[3], "views": result[4], "contents": result[5]}
    # board_detail.html 템플릿에 데이터(bd)를 담아 응답
    return templates.TemplateResponse("board_detail.html", {"request": request, "bd": board})

#--------------------
# --- 회원 관리 기능 ---
#--------------------

#-----------------------------------------------------------
# 회원가입 페이지: 사용자가 회원 정보를 입력할 수 있는 폼(HTML)을 반환
#-----------------------------------------------------------
@app.get("/join", response_class=HTMLResponse)
async def join_form(request: Request):
    return templates.TemplateResponse("join.html", {"request": request})

#-----------------------------------------------------------
# 회원가입 처리: 사용자가 입력한 데이터를 DB에 저장하고 로그인 페이지로 리다이렉트
#-----------------------------------------------------------
@app.post("/join", response_class=HTMLResponse)
async def joinok(request: Request, username: str = Form(...), password: str = Form(...),
                 name: str = Form(""), email: str = Form("")):
    try:
        # 비동기 방식으로 회원 데이터베이스에 연결
        async with aiosqlite.connect(MemberDB_NAME) as db:
            # SQL INSERT 문을 실행하여 새로운 회원 정보 저장
            await db.execute("INSERT INTO member (username, password, name, email) VALUES (?, ?, ?, ?)",
                             (username, password, name, email))
            await db.commit() # 변경사항 반영
    except sqlite3.IntegrityError:
        # 아이디나 이메일 중복 시 발생하는 예러를 잡아 회원가입 폼으로 다시 보냄
        return templates.TemplateResponse("join.html", {"request": request, "error": "중복된 정보입니다."})

    # 회원가입 성공 시 로그인 페이지로 이동
    return RedirectResponse(url="/login", status_code=303)

#-----------------------------------------------------------
# 회원 목록 조회: 저장된 모든 회원 정보를 가져와서 리스트 형태의 페이지로 노출
#-----------------------------------------------------------
@app.get("/list", response_class=HTMLResponse)
async def member_list(request: Request):
    async with aiosqlite.connect(MemberDB_NAME) as db:
        # 최근 가입한 순서(내림차순)로 회원 목록 조회
        async with db.execute("SELECT memberid, username, name, email, regdate FROM member ORDER BY memberid DESC") as cur:
            results = await cur.fetchall()

    # 조회된 튜플 데이터를 템플릿에서 쓰기 편하게 딕셔너리 리스트로 변환
    members = [{"memberid": r[0], "username": r[1], "name": r[2], "email": r[3], "regdate": r[4]} for r in results]
    return templates.TemplateResponse("list.html", {"request": request, "members": members})

#-----------------------------------------------------------
# 로그인 페이지: 아이디와 비밀번호를 입력받는 로그인 폼(HTML)을 반환
#-----------------------------------------------------------
@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

#-----------------------------------------------------------
# 로그인 처리: 입력받은 정보가 DB에 있는지 확인 후 성공 시 게시판으로 이동
#-----------------------------------------------------------
@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    async with aiosqlite.connect(MemberDB_NAME) as db:
        # 아이디와 비밀번호가 일치하는 행이 있는지 조회
        async with db.execute("SELECT username, name FROM member WHERE username=? AND password=?",
                              (username, password)) as cur:
            member = await cur.fetchone()

    # 일치하는 회원이 없는 경우 로그인 실패 메시지와 함께 로그인 페이지 다시 노출
    if member is None:
        return templates.TemplateResponse("login.html", {"request": request, "error": "로그인 실패"})

    # 로그인 성공 시 메시지 페이지 대신 곧바로 게시판 목록으로 이동
    return RedirectResponse(url="/board", status_code=303)

#-----------------------------------------------------------
# 앱 실행부: 서버를 가동하고 코드 변경 시 자동 재시작(reload) 설정
#-----------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    # uvicorn.run("파일명:객체명") 형식을 지켜야 하며 reload 모드 사용 시 중요함
    uvicorn.run("04bMemberBoard_FastAPI:app", host="0.0.0.0", port=8000, reload=True)