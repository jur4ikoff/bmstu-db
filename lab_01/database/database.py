from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import func, text
from datetime import datetime
from typing import Annotated

from config import get_db_url, CREATE_SQL, COPY_SQL, DROP_SQL, LIMITATION_SQL

DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class DataBase:
    def __init__(self):
        pass

    @classmethod
    def parse_sql_file(cls, filepath):
        with open(filepath, "r") as f:
            content = f.read()

        queries = []
        for query in content.split(";"):
            query = query.strip()

            if query and not query.startswith("--"):
                queries.append(query + ";")

        return queries

    async def create_tables(self):
        with open(file=CREATE_SQL, mode="r", encoding="utf-8") as file:
            sql_content = file.read()

        async with async_session_maker() as session:
            statements = sql_content.split(";")
            for statement in statements:
                statement.strip()
                if statement:
                    await session.execute(text(statement))
            print(1)
            await session.commit()

    async def copy_tables(self):
        with open(COPY_SQL, "r") as f:
            content = f.read()
        
        async with async_session_maker() as session:
            await session.execute(text(content))
            await session.commit()

    async def drop_table(self):
        with open(file=DROP_SQL, mode="r", encoding="utf-8") as file:
            sql_content = file.read()

        async with async_session_maker() as session:
            statements = sql_content.split(";")
            for statement in statements:
                statement.strip()
                if statement:
                    await session.execute(text(statement))

            await session.commit()
