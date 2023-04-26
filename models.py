from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, index=True)
    
    code = Column(String, index=True, unique=True)
    rate = Column(Float)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
