from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy import func, text

from config import get_db_url, CREATE_SQL, COPY_SQL, DROP_SQL, LIMITATION_SQL

DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class DataBase:
    def __init__(self):
        pass

    @classmethod
    def read_sql_file(cls, filepath):
        with open(filepath, mode="r", encoding="utf-8") as f:
            content = f.read()
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
