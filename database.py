from contextlib import contextmanager
from typing import Generator
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker, declarative_base


# Configurações de conexão com MySQL:

MYSQL_USER = "root"
MYSQL_PASSWORD = "83627438Jp*"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
DATABASE_NAME = "locadora_db"

root_engine:Engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/",
    echo=False,
    future=True
)

with root_engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME};"))
    conn.commit()

engine:Engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{DATABASE_NAME}",
    echo=True,
    future=True
)

DBSession:Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
DBModel = declarative_base()

@contextmanager
def get_session() -> Generator:
    session:Session = DBSession()
    try:
        yield session
    finally:
        session.close()