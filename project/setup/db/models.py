from sqlalchemy import Column, DateTime, func, Integer

from project.setup.db import db


class Base(db.Model):
    __abstract__ = True  # нельзя создать экземпляры от этого класса

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, nullable=False, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())
