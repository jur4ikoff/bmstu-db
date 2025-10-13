from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.exc import ResourceClosedError
from sqlalchemy import text, func
from sqlalchemy.orm import mapped_column, DeclarativeBase, declared_attr
from datetime import datetime
from typing import Annotated

from config import get_db_url, CREATE_SQL, COPY_SQL, DROP_SQL, LIMITATION_SQL

DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime,  mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now())]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """@declared_attr.directive – декоратор SQLAlchemy, указывающий, 
        что метод определяет метаданные таблицы (а не обычный атрибут).

        Берёт имя класса (cls.__name__), переводит в нижний регистр
        (lower())
        """
        return f"{cls.__name__.lower()}"
    
class DataBase:
    def __init__(self):
        pass

    @classmethod
    def read_sql_file(cls, filepath):
        with open(filepath, mode="r", encoding="utf-8") as f:
            content = f.read()
            return content

    @classmethod
    def read_sql_file_no_comments(cls, filepath):
        with open(filepath, mode="r", encoding="utf-8") as f:

            content = []

            line = f.readline()
            while line:
                if line.startswith("--") or not line:
                    line = f.readline()
                    continue

                content.append(line)
                line = f.readline()

            content = "".join(content)
            return content

    @classmethod
    def parse_sql(cls, response):
        content = response.split(";")

        return content

    async def create_tables(self):
        create_contents = self.read_sql_file(CREATE_SQL)
        create_contents = self.parse_sql(create_contents)

        limitations_contents = self.read_sql_file(LIMITATION_SQL)
        limitations_contents = self.parse_sql(limitations_contents)

        async with async_session_maker() as session:
            for create_content in create_contents:
                await session.execute(text(create_content))

            for limitation_content in limitations_contents:
                await session.execute(text(limitation_content))

            await session.commit()

    async def copy_tables(self):
        content = self.read_sql_file(COPY_SQL)
        content = content.split(";")

        async with async_session_maker() as session:
            for i in content:
                i.strip()
                if i == "'" or not i:
                    continue

                if i[-1] == "'":
                    i += ";'"

                await session.execute(text(i))

            await session.commit()

    async def drop_table(self):
        content = self.read_sql_file(DROP_SQL)

        async with async_session_maker() as session:
            await session.execute(text(content))
            await session.commit()

    async def dml_run(self, filepath: str):
        if filepath.endswith("11.sql") or filepath.endswith("17.sql"):
            return

        content = self.read_sql_file_no_comments(filepath)

        async with async_session_maker() as session:
            print(f"\033[92mЗапрос из файла: {filepath}\033[0m")
            try:
                response = await session.execute(text(content))
                print(response.fetchall())
                print("___________________________________\n\n")
            except ResourceClosedError as e:
                print("success")
