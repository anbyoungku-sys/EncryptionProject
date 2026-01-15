from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from settings import templates, MemberDB_NAME
import aiosqlite, sqlite3

# member 라우트 설정
router = APIRouter(prefix="/member", tags=["member"])

#-----------------------------------------------------------
# 회원가입 페이지: 사용자가 회원 정보를 입력할 수 있는 폼(HTML)을 반환
#-----------------------------------------------------------
@router.get("/join", response_class=HTMLResponse)
async def join_form(request: Request):
    return templates.TemplateResponse("member/join.html", {"request": request})

#-----------------------------------------------------------
# 회원가입 처리: 사용자가 입력한 데이터를 DB에 저장하고 로그인 페이지로 리다이렉트
#-----------------------------------------------------------
@router.post("/join", response_class=HTMLResponse)
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
        return templates.TemplateResponse("member/join.html", {"request": request, "error": "중복된 정보입니다."})

    # 회원가입 성공 시 로그인 페이지로 이동
    return RedirectResponse(url="/login", status_code=303)

#-----------------------------------------------------------
# 회원 목록 조회: 저장된 모든 회원 정보를 가져와서 리스트 형태의 페이지로 노출
#-----------------------------------------------------------
@router.get("/list", response_class=HTMLResponse)
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
@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("member/login.html", {"request": request})

#-----------------------------------------------------------
# 로그인 처리: 입력받은 정보가 DB에 있는지 확인 후 성공 시 게시판으로 이동
#-----------------------------------------------------------
@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    async with aiosqlite.connect(MemberDB_NAME) as db:
        # 아이디와 비밀번호가 일치하는 행이 있는지 조회
        async with db.execute("SELECT username, name FROM member WHERE username=? AND password=?",
                              (username, password)) as cur:
            member = await cur.fetchone()

    # 일치하는 회원이 없는 경우 로그인 실패 메시지와 함께 로그인 페이지 다시 노출
    if member is None:
        return templates.TemplateResponse("member/login.html", {"request": request, "error": "로그인 실패"})

    # 로그인 성공 시 메시지 페이지 대신 곧바로 게시판 목록으로 이동
    return RedirectResponse(url="/board", status_code=303)
