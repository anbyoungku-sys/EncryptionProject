from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from settings import SungJukDB_NAME, templates
import aiosqlite

router = APIRouter(prefix="/sungjuk", tags=["sungjuk"])

@router.get("/list", response_class=HTMLResponse)
async def sungjuk_list(request: Request):
    pass
# 데이터 입력
@router.get("/new", response_class=HTMLResponse)
async def sungjuk_newform(request: Request):
    pass
# 데이터 저장
@router.post("/new", response_class=HTMLResponse)
async def sungjuk_new(request: Request,
                      name: str = Form(...),
                      kor: str = Form(...), eng: str = Form(...), mat: str = Form(...),):
    pass

@router.get("/{sjno}", response_class=HTMLResponse)
async def sungjuk_detail(request: Request, sjno: int):
    pass

# 삭제
@router.get("/{sjno}/delete", response_class=HTMLResponse)
async def sungjuk_delete(sjno: int):
    pass

# 수정
@router.get(path="/{sjno}/edit", response_class=HTMLResponse)
async def sungjuk_editform(request: Request, sjno: int):
    pass

@router.post(path="/{sjno}/edit", response_class=HTMLResponse)
async def sungjuk_edit(request: Request, sjno: int,
       kor: int = Form(...), eng: int = Form(...), mat: int = Form(...)):
    pass
