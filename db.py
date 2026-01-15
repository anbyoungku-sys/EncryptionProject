# 데이터베이스 초기화 관련 함수 정의
from settings import BoardDB_NAME, MemberDB_NAME
import aiosqlite


async def init_db():
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

