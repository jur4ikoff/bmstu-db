from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import mapped_column, DeclarativeBase, declared_attr
from typing import Annotated

from config import get_db_url

DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


int_pk = Annotated[int, mapped_column(primary_key=True)]


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
