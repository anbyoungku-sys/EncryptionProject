# # fastapi 패키지에서 FastAPI 클래스를 가져옵니다.
# from fastapi import FastAPI
#
# app = FastAPI()  # 전체 웹 서버 객체 생성
#
# @app.get("/")  # HTTP GET 요청이 루트 경로("/")로 오면 아래 함수 실행
# async def json_hello():
#     return {"message": "Hello, World!"}  # 딕셔너리를 반환하면 자동으로 JSON으로 변환됨

# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse # 1. HTMLResponse를 가져옵니다.
#
# app = FastAPI()
#
# @app.get("/")
# async def json_hello():
#     long_mes = """
#     #################
#     #   ^       ^   #
#     #       V       #
#     #   #########   #
#     #################
#     """
#     # 2. f-string을 사용하여 <pre> 태그 안에 얼굴을 넣습니다.
#     # 이렇게 하면 브라우저가 줄바꿈을 인식해서 출력합니다.
#     return HTMLResponse(content=f"<pre>{long_mes}</pre>")


# 파일명은 여전히 01Hello_FastAPI!

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, HTMLResponse

app = FastAPI()

@app.get("/")
async def json_hello():
    # JSON으로 응답
    return {"message": "01 Hello, World!"}

@app.get("/thello", response_class=PlainTextResponse)
def text_hello():
    # 텍스트로 응답
    return "01 text_hello, World!"

@app.get("/hhello", response_class=HTMLResponse)
def html_hello():
    # html로 응답
    html_content = """
		<!DOCTYPE html>
		<html>
		    <head>
		        <title>😊Hello Page</title>
		    </head>
		    <body>
		        <h1>01 html_hello, World!</h1>
		        <p>FastAPI로 만든 HTML 페이지입니다.</p>
		    </body>
		</html>
		"""
    return html_content


# 스크립트를 직접 실행할 때만 서버 실행
if __name__ == "__main__":
    import uvicorn  # uvicorn을 직접 임포트해서 사용
    uvicorn.run('01Hello_FastAPI:app', host="0.0.0.0", port=8000, reload=True)

