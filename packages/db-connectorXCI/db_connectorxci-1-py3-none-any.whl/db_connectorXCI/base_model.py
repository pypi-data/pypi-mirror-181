from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import func
# from . import db

class Model(object):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    create_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    update_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        """
            converts model to dict
        """
        return {c.name : getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls, dict:dict)->object:
        """
            return model object from a dictionary
        """
        # columns = (dict.get(col, None) for col in dict.keys())
        # print(columns)
        return cls(**dict)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} object: ID = {self.id}, created at: {self.create_date}"
    __str__ = __repr__

    # @classmethod
    # def all(cls):
    #     objects = db.session.query(cls).all()
    #     return objects
    # @classmethod
    # def first(cls):
    #     return db.session.query(cls).first()
    # @classmethod
    # def filter_by(cls, **kw):
    #     return db.session.query(cls).filter_by(**kw)