from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime
from typing import Annotated

from config import get_db_url

DATABASE_URL = get_db_url()



engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class DataBase:
    def __init__(self):
        pass

    def create_tables(self):
        try:
            f = open()
        except Exception as e:
            print(e)
            raise e