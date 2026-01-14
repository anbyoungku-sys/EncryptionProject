# 파일명은 02Jinja2_FastAPI로 작성할 것!
# pip install jinja2

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi import Form
from cipher_lib.caesar_cipher_v2 import caesar_cipher
from cipher_lib.vigenere_cipher import vigenere_cipher
from cipher_lib.playfare_cipher2 import prepare_text, create_playfair_matrix, playfair_encrypt
from cipher_lib.rsa_cipher import rsa_encrypt


# FastAPI 인스턴스 생성
app = FastAPI()

# 템플릿 엔진 설정 및 templates 폴더 경로 지정
templates = Jinja2Templates(directory="templates")


# 루트 경로("/jhello")에 GET 요청이 들어오면 실행될 함수 정의
@app.get("/jhello")
def json_hello():
    return {"message": "02 Hello, World!"}


# 별도의 HTML 파일을 사용해서 웹 페이지를 렌더링
# 보통 Jinja2 템플릿 엔진을 사용하며, templates 폴더를 만들어 HTML 파일을 두고 렌더링
@app.get("/j2hello", response_class=HTMLResponse)
def jinja2_hello(request: Request):
    # TemplateResponse(템플릿파일명, 템플릿에_전달할_데이터)
    # 템플릿 컨텍스트 - HTML 안에서 사용할 수 있는 변수들의 집합
    # json : 자바스크립트를 이용한 데이터를 표현하는 형식 {이름 : 값, 이름:값}
    # {}에 '키:값' 쌍으로 데이터들을 정의
    return templates.TemplateResponse("j2hello.html",
        {"request": request, "message": "❤️J2Hello, World!"})


# GET 요청: 로그인 폼 보여주기
@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# POST 요청: 폼 데이터 처리
@app.post("/login", response_class=HTMLResponse)
# username, password는 Form 데이터에서 문자열 타입으로 필수 입력 값이다
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    # username과 password 값을 템플릿으로 전달
    form = await request.form()
    # 암호화 처리
    # 시저암호화
    ceasar_encrypted = caesar_cipher(password, 5)

    # 비즈네르 암호화
    vigen_encrypted = vigenere_cipher(password, "KEY")

    # 플레이페어 암호화
    # 1. 텍스트 준비 (2글자씩 나누기)
    pairs = prepare_text(password)
    # 2. 5x5 행렬 생성 (키는 "321olleh" 등으로 지정)
    table = create_playfair_matrix("321olleh")
    # 3. 암호화 실행 (결과는 리스트 형태로 반환됨)
    playfair_list = playfair_encrypt(pairs, table)
    # 4. 리스트를 문자열로 합치기 (HTML에서 보기 좋게)
    playfair_res = "".join(playfair_list)

    # MD5 암호화 비밀번호: 321olleh

    # SHA-256 암호화 비밀번호: 321olleh

    # DES 암호화 비밀번호: 321olleh

    # AES 암호화 비밀번호: 321olleh

    # RSA 암호화 비밀번호: 321olleh
    rsa_res = rsa_encrypt(password, "321olleh")




    return templates.TemplateResponse("loginok.html", {
        "request": request,
        "form": form,
        "username": username,
        "password": password,
        "ceasar_encrypted" : ceasar_encrypted,
        "vigen_encrypted" : vigen_encrypted,
        "playfair_encrypted": playfair_res,
        "rsa_encrypted": rsa_res,

    })


# 스크립트를 직접 실행할 때만 서버 실행
if __name__ == "__main__":
    import uvicorn  # uvicorn을 직접 임포트해서 사용
    uvicorn.run('02Jinja2_FastAPI:app', host="0.0.0.0", port=8000, reload=True)







