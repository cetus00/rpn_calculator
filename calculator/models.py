
from sqlalchemy import Column, Integer, ARRAY, Numeric, TIMESTAMP, func, Float
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class Stacks(Base):
    id: int = Column("id", Integer, primary_key=True)
    stack: list[float] = Column("stack", ARRAY(Float), server_default='{}', default=[])